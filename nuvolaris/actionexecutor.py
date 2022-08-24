# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import os, logging, json
import nuvolaris.config as cfg
import nuvolaris.couchdb_util as cu
import nuvolaris.kube as kube
import croniter as cn
import requests as req
from datetime import datetime

def check(f, what, res):
    if f:
        logging.info(f"OK: {what}")
        return res and True
    else:
        logging.warn(f"ERR: {what}")
        return False

#
# extract the configured interval between
# two consecutive execution of this process
# scheduled via the nuvolaris cron component
#
def from_cron_to_seconds(base, cronExpr):
    """
        >>> import nuvolaris.actionexecutor as ae
        >>> from datetime import datetime
        >>> base = datetime.now()
        >>> ae.from_cron_to_seconds(base,'* * * * *')
        60.0
        >>> ae.from_cron_to_seconds(base,'*/30 * * * *')
        1800.0
    """    
    itr = cn.croniter(cronExpr, base)
    nextTime1 = itr.get_next(datetime)
    nextTime2 = itr.get_next(datetime)
    diff = nextTime2 - nextTime1
    return diff.total_seconds()

#
# Check if an action with the specified cron expression
# should have been triggered since the last execution of this scheduled job.
#
def action_should_trigger(currentDate, executionInterval, actionCronExpression):
    """
        >>> import nuvolaris.actionexecutor as ae
        >>> from datetime import datetime
        >>> base = datetime.now()
        >>> base1 = datetime(2022, 8, 6, 16, 30, 0, 0)          
        >>> base2 = datetime(2022, 8, 6, 16, 00, 0, 0) 
        >>> base3 = datetime(2022, 8, 6, 16, 3, 0, 0)
        >>> base4 = datetime(2022, 8, 6, 16, 10, 0, 0) 
        >>> ae.action_should_trigger(base,60,'* * * * *')
        True
        >>> ae.action_should_trigger(base1, 60,'*/30 * * * *')
        True
        >>> ae.action_should_trigger(base2, 60,'*/30 * * * *')
        True
        >>> ae.action_should_trigger(base3, 60,'*/5 * * * *')
        False
        >>> ae.action_should_trigger(base4, 60,'*/5 * * * *')
        True
    """ 
    currentTimestamp = datetime.timestamp(currentDate)
    prevTimestamp = currentTimestamp - executionInterval
    prevDate = datetime.fromtimestamp(prevTimestamp)

    result = False

    for dt in cn.croniter_range(prevDate, currentDate, actionCronExpression):
        if(dt):
            result = True
            break

    return result

#
# query the dbn database using the specified selecto
#
def find_docs(db, dbn, selector, username, password):
    documents = []
    query = json.loads(selector)
    logging.info(f"Querying couchdb {dbn} for documents")

    #CouchDB returns no more than 25 records. We iterate to get all the cron enabled actions.
    while(True):
        logging.info(f"select query param {json.dumps(query)}")
        res = db.find_doc(dbn, json.dumps(query), username, password)

        if(res == None):
            break

        if(res['docs']):
            docs = list(res['docs'])
            if(len(docs) > 0):
                documents.extend(docs)
                if(res['bookmark']):
                    query['bookmark']=res['bookmark']                
            else:
                logging.info('docs item is an emtpy list. No more documents found')
                break 
        else:
            logging.info('docs items not present. no more documents found')
            break 
       
    return list(documents)

#
# Get subject from nuvolaris_subjects db
#
#TODO need to find a way to build a dictionary with dynamic key or a hashmap
def get_subjects(db, username, password):
    subjects = []
    selector = '{"selector":{"subject": {"$exists": true}},"fields":["namespaces"]}'
    namespaces = find_docs(db, "subjects", selector, username, password)

    for entry in namespaces:
        currentNamespaceList = list(entry['namespaces'])
        for namespace in currentNamespaceList:            
            subjects.append(namespace);            

    return list(subjects)

#
# get actions from the nuvolaris_whisks db
#
def get_cron_aware_actions(db, username, password):
    selector = '{"selector":{"entityType":"action", "annotations": {"$elemMatch": {"key": "cron"}}}, "fields": ["_id", "annotations", "name", "_rev","namespace","parameters","entityType"]}'
    return find_docs(db, "whisks", selector, username, password)
#
# POST a request to invoke the ow action
#
def call_ow_action(url, parameters, ow_auth):
    logging.info(f"POST request to {url}")
    headers = {'Content-Type': 'application/json'}

    try:
        response = None
        if(len(parameters)>0):
            response = req.post(url, auth=(ow_auth['username'],ow_auth['password']), headers=headers, data=json.dumps(parameters))
        else:
            #If the body is empty Content-Type must be not provided otherwise OpenWhisk api returns a 400 error    
            response = req.post(url, auth=(ow_auth['username'],ow_auth['password']))

        if (response.status_code in [200,202]):
            logging.info(f"call to {url} succeeded with {response.status_code}. Body {response.text}")
            return True        
            
        logging.warn(f"query to {url} failed with {response.status_code}. Body {response.text}")
        return False
    except Exception as inst:
        logging.warn(f"Failed to invoke action {type(inst)}")
        logging.warn(inst)
        return False        
    
#
# Evaluate if the given whisk action must be executed or not
# 
# dAction input is a json Object with similar structure.
# 
# dAction = '{"_id":"nuvolaris/hello-cron-action","annotations":[{"key":"cron","value":"*/2 * * * *"},{"key":"provide-api-key","value":false},{"key":"exec","value":"nodejs:14"}],"name":"hello-cron-action","_rev":"1-19f424e1fec1c02a2ecccf6f90978e31","namespace":"nuvolaris","parameters":[],"entityType":"action"}'
def handle_action(baseurl, currentDate, executionInterval, dAction, subjects):  
    actionName = dAction['name']
    entityType = dAction['entityType']
    actionNamespace = dAction['namespace']
    actionParameters = list(dAction['parameters'])
    actionAnnotations = list(dAction['annotations'])
    actionCronExpression = " "    

    for a in actionAnnotations:
        if(a['key'] == 'cron'):
            actionCronExpression = a['value']
 
    if not cn.croniter.is_valid(actionCronExpression):
        logging.warn(f"action {actionNamespace}/{actionName} cron expression {actionCronExpression} is not valid. Skipping execution")
        return None

    if not action_should_trigger(currentDate, executionInterval, actionCronExpression):
        logging.warn(f"action {actionNamespace}/{actionName} cron expression {actionCronExpression} does not trigger an execution at {currentDate}")
        return None

    subjectName = actionNamespace.split("/")[0]
    auth = get_auth(subjects, subjectName)
    if(auth):
        call_ow_action(f"{baseurl}{actionNamespace}/actions/{actionName}?blocking=false&result=false", actionParameters, auth)
    else:
        logging.warn('No subject {subjectName} credentials found!')
    return None

#
# Search and return a {'username':'xxx','passowrd':'xxx'} dictionary
#
def get_auth(subjects, subjectName):
    for subject in subjects:
        if(subject['name'] == subjectName):
            return {'username':subject['uuid'], 'password':subject['key']}
        
    return None


#
# Will queries the internal CouchDB for cron aware actions
# to be triggered since the last execution time.
# TODO the interval execution time must be parametrized.
# Implement the logic to query for actions and evaluate how to execute them
#
def start():
    # load nuvolaris config from the named crd
    config = os.environ.get("NUVOLARIS_CONFIG")
    if config:        
        logging.basicConfig(level=logging.INFO)
        spec = json.loads(config)
        cfg.configure(spec)
        for k in cfg.getall(): logging.info(f"{k} = {cfg.get(k)}")

    currentDate = datetime.now()
    interval = from_cron_to_seconds(currentDate, cfg.get('scheduler.schedule'))
    logging.info(f"interval in seconds between 2 execution is {interval} seconds")

    db = cu.CouchDB()
    res = check(db.wait_db_ready(30), "wait_db_ready", True)

    if(res):
        ow_protocol = cfg.get('controller.protocol') or "http"
        ow_host = cfg.get('controller.host') or "controller"
        ow_port = cfg.get('controller.port') or "3233"
        baseurl = f"{ow_protocol}://{ow_host}:{ow_port}/api/v1/namespaces/"                
        actions = get_cron_aware_actions(db, cfg.get('couchdb.controller.user'),cfg.get('couchdb.controller.password'))

        if(len(actions) > 0):
            subjects = get_subjects(db, cfg.get('couchdb.controller.user'),cfg.get('couchdb.controller.password'))
            for action in actions:
                handle_action(baseurl, currentDate, interval, action, subjects)
        else:
            logging.info('No cron aware action extracted. Exiting....')
    else:
        logging.warn("CouchDB it is not available. Exiting....")
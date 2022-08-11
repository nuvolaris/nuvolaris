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

def get_cron_aware_actions(db, username, password):
    actions = []
    dbn = "whisks"
    query = json.loads('{"selector":{"entityType":"action", "annotations": {"$elemMatch": {"key": "cron"}}}, "fields": ["_id", "annotations", "name", "_rev","namespace","parameters"]}')
    logging.info(f"Querying couchdb {dbn} for actions")

    #CouchDB returns no more than 25 records. We iterate to get all the cron enabled actions.
    while(True):
        logging.info(f"select query param {json.dumps(query)}")
        res = db.find_doc(dbn, json.dumps(query), username, password)
        logging.info(f"couchdb response {json.dumps(res)}")

        if(res == None):
            break

        if(res['docs']):
            docs = list(res['docs'])
            if(len(docs) > 0):
                actions.extend(docs)
                if(res['bookmark']):
                    query['bookmark']=res['bookmark']                
            else:
                logging.info('docs item is an emtpy list. No more actions found')
                break 
        else:
            logging.info('docs items not present. no more actions found')
            break 
       
    return list(actions)


#
# Evaluate if the given whisk action must be executed or not
# 
# jAction input is a json Object with similar structure.
# 
# jAction = '{"_id":"nuvolaris/hello-cron-action","annotations":[{"key":"cron","value":"*/2 * * * *"},{"key":"provide-api-key","value":false},{"key":"exec","value":"nodejs:14"}],"name":"hello-cron-action","_rev":"1-19f424e1fec1c02a2ecccf6f90978e31","namespace":"nuvolaris","parameters":[]}'
def handle_action(currentDate, executionInterval, jAction):  
    actionName = jAction['name']
    actionNamespace = jAction['namespace']
    actionParameter = list(jAction['parameters'])
    actionAnnotations = list(jAction['annotations'])
    actionCronExpression = " "

    for a in actionAnnotations:
        if(a['key'] == 'cron'):
            actionCronExpression = a['value']

    logging.info(f"Evaluating cron expression {actionCronExpression} for action {actionNamespace}/{actionName}")    

    if not cn.croniter.is_valid(actionCronExpression):
        logging.warn(f"cron expression {actionCronExpression} for action {actionNamespace}/{actionName} is not a valid one. Exiting evaluation")
        return None
    
    shouldTrigger = action_should_trigger(currentDate, executionInterval, actionCronExpression)

    if not shouldTrigger:
        logging.warn(f"cron expression {actionCronExpression} for action {actionNamespace}/{actionName} does not trigger execution at {currentDate}")
        return None

    #TODO call action trigger
    logging.info(f"triggering call for action {actionNamespace}/{actionName} at {currentDate}")
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

    base = datetime.now()
    interval = from_cron_to_seconds(base, cfg.get('scheduler.schedule'))   

    logging.info(f"interval in seconds between 2 execution is {interval} seconds")

    db = cu.CouchDB()
    res = check(db.wait_db_ready(60), "wait_db_ready", True)

    if(res):        
        actions = get_cron_aware_actions(db, cfg.get('couchdb.controller.user'),cfg.get('couchdb.controller.password'))
        if(len(actions) > 0):
            for action in actions:
                handle_action(base, interval, action)
        else:
            logging.info('No cron aware action extracted. Exiting....')
    else:
        logging.warn("CouchDB it is not available. Exiting....")
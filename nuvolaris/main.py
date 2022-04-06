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
import kopf
import logging
import json, flatdict, os, os.path
import nuvolaris.config as cfg
import nuvolaris.kube as kube
import nuvolaris.couchdb as couchdb
import nuvolaris.mongodb as mongodb
import nuvolaris.bucket as bucket
import nuvolaris.openwhisk as openwhisk

# tested by an integration test
@kopf.on.login()
def login(**kwargs):
    token = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    if os.path.isfile(token):
        logging.debug("found serviceaccount token: login via pykube in kubernetes")
        return kopf.login_via_pykube(**kwargs)
    logging.debug("login via client")
    return kopf.login_via_client(**kwargs)

# tested by an integration test
@kopf.on.create('nuvolaris.org', 'v1', 'whisks')
def whisk_create(spec, name, **kwargs):
    cfg.configure(spec, name)

    state = {
        "openwhisk": "?",  # Openwhisk Controller or Standalone
        "invoker": "?",  # Invoker
        "couchdb": "?",  # Couchdb
        "kafka": "?",  # Kafka
        "redis": "?",  # Redis
        "mongodb": "?",  # MongoDB
        "s3bucket": "?"   # S3-compatbile buckets
    }

    if cfg.get('components.couchdb'):
        state['couchdb']= "starting"
        couchdb.create()
    else:
        state['couchdb'] = "off"

    if cfg.get('components.kafka'):
        logging.warn("invoker not yet implemented")
        state['kafka'] = "n/a"
    else:
        state['kafka'] = "off"

    if cfg.get('components.openwhisk'):
        state['openwhisk'] = "starting"
        openwhisk.create()        
    else:
        state['openwhisk'] = "off"

    if cfg.get('components.invoker'):
        logging.warn("invoker not yet implemented")
        state['invoker'] = "n/a"
    else:
        state['invoker'] = "off"

    if cfg.get('components.mongodb'):
        logging.warn("invoker not yet implemented")
        state['mongodb'] = "n/a"
    else:
        state['mongodb'] = "off"

    if cfg.get('components.redis'):
        logging.warn("invoker not yet implemented")
        state['redis'] = "n/a"
    else:
        state['redis'] = "off"

    if cfg.get('components.s3bucket'):
        logging.warn("invoker not yet implemented")
        state['s3bucket'] = "n/a"
    else:
        state['s3bucket'] = "off"

    #message = []
    #bucket.create()
    #mongodb.create()
    #mongodb.init()
    #message.append(openwhisk.create())
    #msg = "\n".join(message)
    #logging.debug(msg)
    #print(json.dumps(spec, indent=4))
    return state

# tested by an integration test
@kopf.on.delete('nuvolaris.org', 'v1', 'whisks')
def whisk_delete(spec, **kwargs):
    message = []
    message.append(openwhisk.delete())
    message.append(openwhisk.cleanup())
    #mongodb.delete()
    #couchdb.delete()
    #bucket.delete()
    msg = "\n".join(message)
    logging.debug(msg)
    return msg

# tested by integration test
@kopf.on.field("service", field='status.loadBalancer')
def service_update(old, new, name, **kwargs):
    nodeLabels = kube.kubectl("get", "nodes", jsonpath='{.items[].metadata.labels}')
    ingress = []
    if "ingress" in new and len(new['ingress']) >0:
        ingress = new['ingress']
    
    apihost = openwhisk.apihost(ingress, nodeLabels)
    openwhisk.annotate(f"apihost={apihost}")

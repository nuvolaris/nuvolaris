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
import nuvolaris.redis as redis
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
    print("***", name)

    cfg.clean()
    cfg.configure(spec)
    cfg.detect()
    for k in cfg.getall(): logging.info(f"{k} = {cfg.get(k)}")
    owner = kube.get(f"wsk/{name}")

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
        try:
            msg = couchdb.create(owner)
            state['couchdb']= "on"
            logging.info(msg)
        except:
            logging.exception("cannot create couchdb")
            state['couchdb']= "error"
    else:
        state['couchdb'] = "off"

    if cfg.get('components.redis'):
        try:
            msg = redis.create(owner)
            state['redis'] = "on"
            logging.info(msg)
        except:
            exception("cannot create redis")
            state['redis']= "error"
    else:
        state['redis'] = "off"

    if cfg.get('components.openwhisk'):
        try:
            msg = openwhisk.create(owner)
            state['openwhisk'] = "on"
            logging.info(msg)
        except:
            exception("cannot create openwhisk")
            state['openwhisk']= "error"
    else:
        state['openwhisk'] = "off"

    if cfg.get('components.kafka'):
        logging.warn("invoker not yet implemented")
        state['kafka'] = "n/a"
    else:
        state['kafka'] = "off"

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


    if cfg.get('components.s3bucket'):
        logging.warn("invoker not yet implemented")
        state['s3bucket'] = "n/a"
    else:
        state['s3bucket'] = "off"

    return state

# tested by an integration test
@kopf.on.delete('nuvolaris.org', 'v1', 'whisks')
def whisk_delete(spec, **kwargs):
    logging.info("whisk_delete")

    if cfg.get("components.redis"):
        msg = redis.delete()
        logging.info(msg)

    if cfg.get('components.couchdb'):
        msg = couchdb.delete()
        logging.info(msg)

    if cfg.get("components.openwhisk"):
        msg = openwhisk.delete()
        logging.info(msg)


# tested by integration test
@kopf.on.field("service", field='status.loadBalancer')
def service_update(old, new, name, **kwargs):    
    if not name == "apihost":
        return

    logging.debug(f"service_update: {json.dumps(new)}")
    ingress = []
    if "ingress" in new and len(new['ingress']) >0:
        ingress = new['ingress']
    
    apihost = openwhisk.apihost(ingress)
    openwhisk.annotate(f"apihost={apihost}")

#@kopf.on.field("sts", field='status.availableReplicas')
def deploy_update(old, new, name, **kwargs):
    if not name == "couchdb":
        return 

    logging.debug("deploy_update: old={old} new={new}")
    if new == 1:
        data = {
            "host": cfg.get("couchdb.host") or "couchdb",
            "port": cfg.get("couchdb.port") or "5984",
            "admin_user": cfg.get("couchdb.admin.user"),
            "admin_password": cfg.get("couchdb.admin.password"),
            "controller_user": cfg.get("couchdb.controller.user"),
            "controller_password": cfg.get("couchdb.controller.password"),
            "invoker_user": cfg.get("couchdb.invoker.user"),
            "invoker_password": cfg.get("couchdb.invoker.password")
        }
        logging.debug(data)
        logging.info(kube.applyTemplate("couchdb-init.yaml", data))

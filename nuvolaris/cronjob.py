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
import kopf, logging, json
import nuvolaris.kube as kube
import nuvolaris.kustomize as kus
import nuvolaris.config as cfg

def create(owner=None):
    logging.info("creating cron")
    
    img = cfg.get('operator.image') or "missing-operator-image"
    tag = cfg.get('operator.tag') or "missing-operator-tag"
    image = f"{img}:{tag}"
    logging.info(f"cron using image {image}")

    #default to every minutes if not configured
    schedule = cfg.get('scheduler.schedule') or "* * * * *"

    config = json.dumps(cfg.getall())
    data = {
        "image": image,
        "schedule": schedule,
        "config": config,
        "name": "cron"
    }
    
    kust = kus.patchTemplate("scheduler", "cron-init.yaml", data)    
    spec = kus.kustom_list("scheduler", kust, templates=[], data=data)

    if owner:
        kopf.append_owner_reference(spec['items'], owner)
    else:
        cfg.put("state.cron.spec", spec)

    res = kube.apply(spec)
    logging.info(f"create cron: {res}")
    return res    

def delete():
    spec = cfg.get("state.cron.spec")
    res = False
    if spec:
        res = kube.delete(spec)
        logging.info(f"delete cron: {res}")
    return res
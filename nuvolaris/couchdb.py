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
import kopf, os, logging, json, time
import nuvolaris.kustomize as kus
import nuvolaris.kube as kube
import nuvolaris.couchdb_util as cu
import nuvolaris.config as cfg
import nuvolaris.couchdb_util

def create(owner=None):
    logging.info("create couchdb")
    u = cfg.get('couchdb.admin.user', "COUCHDB_ADMIN_USER", "whisk_admin")
    p = cfg.get('couchdb.admin.password', "COUCHDB_ADMIN_PASSWORD", "some_passw0rd")
    user = f"db_username={u}"
    pasw = f"db_password={p}"

    img = cfg.get('operator.image') or "missing-operator-image"
    tag = cfg.get('operator.tag') or "missing-operator-tag"
    image = f"{img}:{tag}"

    config = json.dumps(cfg.getall())
    data = {
        "image": image,
        "config": config,
        "name": "couchdb", 
        "size": cfg.get("couchdb.volume-size", "COUCHDB_VOLUME_SIZE", 10), 
        "dir": "/opt/couchdb/data",
        "storageClass": cfg.get("nuvolaris.storageClass")
    }

    kust =  kus.secretLiteral("couchdb-auth", user, pasw)
    kust += kus.patchTemplate("couchdb", "set-attach.yaml", data) 
    spec = kus.kustom_list("couchdb", kust, templates=["couchdb-init.yaml"], data=data)
    if owner:
        kopf.append_owner_reference(spec['items'], owner)
    else:
        cfg.put("state.couchdb.spec", spec)
    res = kube.apply(spec)
    logging.info(f"create couchdb: {res}")

def delete():
    spec = cfg.get("state.couchdb.spec")
    res = False
    if spec:
        res = kube.delete(spec)
        logging.info(f"delete couchdb: {res}")
    return res

def check(f, what, res):
    if f:
        logging.info(f"OK: {what}")
        return res and True
    else:
        logging.warn(f"ERR: {what}")
        return False

def init_system(db):
    res = check(db.wait_db_ready(60), "wait_db_ready", True)
    res = check(db.configure_single_node(), "configure_single_node", res)
    res = check(db.configure_no_reduce_limit(), "configure_no_reduce_limit", res)
    cuser = cfg.get('couchdb.controller.user', "COUCHDB_CONTROLLER_USER", "controller_admin")
    cpasw = cfg.get('couchdb.controller.password', "COUCHDB_CONTROLLER_PASSWORD", "s0meP@ass1")
    iuser = cfg.get('couchdb.invoker.user', "COUCHDB_INVOKER_USER", "invoker_admin")
    ipasw = cfg.get('couchdb.incvoker.password', "COUCHDB_INVOKER_PASSWORD", "s0meP@ass2")
    res = check(db.add_user(cuser, cpasw), "add_user: controller", res)
    return check(db.add_user(iuser, ipasw), "add_user: invoker", res)

def init_subjects(db):
    subjects_design_docs = [
        "auth_design_document_for_subjects_db_v2.0.0.json",
        "filter_design_document.json",
        "namespace_throttlings_design_document_for_subjects_db.json"]
    dbn = "subjects"
    res = check(db.wait_db_ready(60), "wait_db_ready", True)
    res = check(db.create_db(dbn), "create_db: subjects", res)
    members = [cfg.get('couchdb.controller.user'), cfg.get('couchdb.invoker.user')]
    res = check(db.add_role(dbn, members), "add_role: subjects", res)
    for i in subjects_design_docs:
        res = check(db.update_templated_doc(dbn, i, {}), f"add {i}", res)
    return res

def init_activations(db):
    activations_design_docs = [
        "whisks_design_document_for_activations_db_v2.1.0.json",
        "whisks_design_document_for_activations_db_filters_v2.1.1.json",
        "filter_design_document.json",
        "activations_design_document_for_activations_db.json",
        "logCleanup_design_document_for_activations_db.json"
    ]
    dbn = "activations"
    res = check(db.wait_db_ready(60), "wait_db_ready", True)
    res = check(db.create_db(dbn), "create_db: activations", res)
    members = [cfg.get('couchdb.controller.user'), cfg.get('couchdb.invoker.user')]
    res = check(db.add_role(dbn, members), "add_role: activations", res)
    for i in activations_design_docs:
        res = check(db.update_templated_doc(dbn, i, {}), f"add {i}", res)
    return res

def init_actions(db):
    whisks_design_docs = [
        "whisks_design_document_for_entities_db_v2.1.0.json",
        "filter_design_document.json"
    ]
    dbn = "whisks"
    res = check(db.wait_db_ready(60), "wait_db_ready", True)
    res = check(db.create_db(dbn), "create_db: whisks", res)
    members = [cfg.get('couchdb.controller.user'), cfg.get('couchdb.invoker.user')]
    res = check(db.add_role(dbn, members), "add_role: actions", res)
    for i in whisks_design_docs:
        res = check(db.update_templated_doc(dbn, i, {}), f"add {i}", res)
    return res

def add_initial_subjects(db):
    res = check(db.wait_db_ready(60), "wait_db_ready", True)
    dbn = "subjects"
    for _, (name, value) in enumerate(cfg.getall("openwhisk.namespaces").items()):
        [uuid, key] = value.split(":")
        basename = name.split(".")[-1]
        data = { "name": basename, "key": key, "uuid": uuid}
        res = check(db.update_templated_doc(dbn, "subject.json", data), f"add {name}", res)
    return res

def init():
    # load nuvolaris config from the named crd
    config = os.environ.get("NUVOLARIS_CONFIG")
    if config:
        import logging
        logging.basicConfig(level=logging.INFO)
        spec = json.loads(config)
        cfg.configure(spec)
        for k in cfg.getall(): logging.info(f"{k} = {cfg.get(k)}")

    # wait for couchdb to be ready
    while not kube.wait("po/couchdb-0", "condition=ready"):
        print("waiting for couchdb-0 ready...")
        time.sleep(1)

    db = nuvolaris.couchdb_util.CouchDB()
    res = check(init_system(db), "init_system", True)
    res = check(init_subjects(db), "init_subjects", res) 
    res = check(init_activations(db), "init_activations", res)
    res = check(init_actions(db), "init_actions", res)
    return check(add_initial_subjects(db), "add_subjects", res)


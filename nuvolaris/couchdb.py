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
import nuvolaris.kustomize as nku
import nuvolaris.kube as kube
import nuvolaris.couchdb_util as cu
import nuvolaris.config as cfg
import nuvolaris.couchdb_util

def create():
    user = f"db_password={cfg.get('couchdb.admin.password')}"
    pasw =  f"db_username={cfg.get('couchdb.admin.user')}"
    secret =  nku.secretLiteral("couchdb-auth", user, pasw)
    spec = nku.kustom_list("couchdb", secret)
    res = kube.apply(spec)
    logging.info(res)
    return res

def delete():
    spec = nku.kustom_list("couchdb")
    res = kube.delete(spec)
    logging.info(res)
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
    res = check(db.add_user(cfg.get('couchdb.controller.user'), cfg.get('couchdb.controller.password')), "add_user: controller", res)
    return check(db.add_user(cfg.get('couchdb.invoker.user'), cfg.get('couchdb.invoker.password')), "add_user: invoker", res)

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
        data = { "name": name, "key": key, "uuid": uuid}
        res = check(db.update_templated_doc(dbn, "subject.json", data), f"add {name}", res)
    return res

def init():
    db = nuvolaris.couchdb_util.CouchDB()
    res = check(init_system(db), "init_system", True)
    res = check(init_subjects(db), "init_subjects", res) 
    res = check(init_activations(db), "init_activations", res)
    res = check(init_actions(db), "init_actions", res)
    return check(add_initial_subjects(db), "add_subjects", res)

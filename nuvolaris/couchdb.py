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

def create():
    spec = nku.kustom_list("couchdb")
    res = kube.apply(spec)
    logging.info(res)
    return res

def delete():
    spec = nku.kustom_list("couchdb")
    logging.info(res)
    res = kube.delete(spec)
    return 

def check(f, what, res):
    if f:
        logging.info(f"OK: {what}")
        return res and True
    else:
        logging.warn(f"ERR: {what}")
        return False

def init_system(config):
    res = check(cu.configure_single_node(), "configure_single_node", True)
    res = check(cu.configure_no_reduce_limit(), "configure_no_reduce_limit", res)
    res = check(cu.add_user(config['couchdb']['controller']['user'], config['couchdb']['controller']['password']), "add_user: controller", res)
    return check(cu.add_user(config['couchdb']['invoker']['user'], config['couchdb']['invoker']['password']), "add_user: invoker", res)

def init_subjects(config):
    subjects_design_docs = [
        "auth_design_document_for_subjects_db_v2.0.0.json",
        "filter_design_document.json",
        "namespace_throttlings_design_document_for_subjects_db.json"]
    db = "subjects"
    res = check(cu.create_db(db), "create_db: subjects", True)
    members = [config['couchdb']['controller']['user'], config['couchdb']['controller']['user']]
    res = check(cu.add_role(db, members), "add_role: subjects", res)
    for i in subjects_design_docs:
        res = check(cu.update_templated_doc(db, i, {}), f"add {i}", res)
    return res

def init_activations(config):
    activations_design_docs = [
        "whisks_design_document_for_activations_db_v2.1.0.json",
        "whisks_design_document_for_activations_db_filters_v2.1.1.json",
        "filter_design_document.json",
        "activations_design_document_for_activations_db.json",
        "logCleanup_design_document_for_activations_db.json"
    ]
    db = "activations"
    res = check(cu.create_db(db), "create_db: activations", True)
    members = [config['couchdb']['controller']['user'], config['couchdb']['controller']['user']]
    res = check(cu.add_role(db, members), "add_role: activations", res)
    for i in activations_design_docs:
        res = check(cu.update_templated_doc(db, i, {}), f"add {i}", res)
    return res

def init_actions(config):
    whisks_design_docs = [
        "whisks_design_document_for_entities_db_v2.1.0.json",
        "filter_design_document.json"
    ]
    db = "whisks"
    res = check(cu.create_db(db), "create_db: whisks", True)
    members = [config['couchdb']['controller']['user'], config['couchdb']['controller']['user']]
    res = check(cu.add_role(db, members), "add_role: actions", res)
    for i in whisks_design_docs:
        res = check(cu.update_templated_doc(db, i, {}), f"add {i}", res)
    return res

def add_subjects(config):
    res = True
    db = "subjects"
    for name in config['openwhisk']['namespaces'].keys():
        [uuid, key] = config['openwhisk']['namespaces'][name].split(":")
        data = { "name": name, "key": key, "uuid": uuid}
        res = check(cu.update_templated_doc(db, "subject.json", data), f"add {name}", res)
    return res

def init(config):
    res = check(init_system(config), "init_system", True)
    res = check(init_subjects(config), "init_subjects", res) 
    res = check(init_activations(config), "init_activations", res)
    res = check(init_actions(config), "init_actions", res)
    return check(add_subjects(config), "add_subjects", res)

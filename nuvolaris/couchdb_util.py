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
import os, json, time, sys, logging
import requests as req

from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader(["./nuvolaris/templates", "./nuvolaris/files"])
env = Environment(loader=loader)
import nuvolaris.config as cfg

class CouchDB:
  def __init__(self):
    self.db_protocol   = "http"
    self.db_prefix     = "nuvolaris_"
    self.db_port       = cfg.get("couchdb.port", "COUCHDB_SERVICE_PORT", "5984")
    self.db_host       = cfg.get("couchdb.host", "COUCHDB_SERVICE_HOST", "localhost")
    self.db_username   = cfg.get("couchdb.admin.user", "COUCHDB_ADMIN_USER", "whisk_admin")
    self.db_password   = cfg.get("couchdb.admin.password", "COUCHDB_ADMIN_PASSWORD", "some_passw0rd")
    self.db_auth = req.auth.HTTPBasicAuth(self.db_username,self.db_password)
    self.db_url = f"{self.db_protocol}://{self.db_host}:{self.db_port}"
    self.db_base = f"{self.db_url}/{self.db_prefix}"

  def wait_db_ready(self, max_seconds):
      start = time.time()
      delta = 0
      while delta < max_seconds:
        try:
          r = req.get(f"{self.db_url}/_utils", timeout=1)
          print(r)
          if r.status_code == 200:
            return True
        except Exception as e:
          #print(e)
          print(f"waiting since: {delta} seconds")
        delta = int(time.time() - start)
        time.sleep(1)
      return False

  # check if database exists, return boolean
  def check_db(self, database):
    url = f"{self.db_base}{database}"
    r = req.head(url, auth=self.db_auth)
    return r.status_code == 200
  
  # delete database, return true if ok
  def delete_db(self, database):
    url = f"{self.db_base}{database}"
    r = req.delete(url, auth=self.db_auth)
    return r.status_code == 200

  # create db, return true if ok
  def create_db(self, database):
    url = f"{self.db_base}{database}"
    r = req.put(url, auth=self.db_auth) 
    return r.status_code == 201

  # database="subjects"
  def recreate_db(self, database, recreate=False):
    msg = "recreate_db:"
    exists = self.check_db(database)
    if recreate and exists:
      msg += " deleted"
      self.delete_db(database)
    if recreate or not exists:
      msg += " created"
      self.create_db(database)
    return msg

  def get_doc(self, database, id, user=None, password="", no_auth=False):
    url = f"{self.db_base}{database}/{id}"
    if no_auth:
      db_auth=None
    elif user:
      db_auth=req.auth.HTTPBasicAuth(user, password)
    else:
      db_auth = self.db_auth
    r = req.get(url, auth=db_auth) 
    if r.status_code == 200:
      return json.loads(r.text)
    return None

  def update_doc(self, database, doc):
    if '_id' in doc:
      url = f"{self.db_base}{database}/{doc['_id']}"
      cur = self.get_doc(database, doc['_id'])
      if cur and '_rev' in cur:
        doc['_rev'] = cur['_rev']
        r = req.put(url, auth=self.db_auth, json=doc)
      else:
        r = req.put(url, auth=self.db_auth, json=doc)
      return r.status_code in [200,201]
    return False

  def delete_doc(self, database, id):
    cur = self.get_doc(database, id)
    if cur and '_rev' in cur:
        url = f"{self.db_base}{database}/{cur['_id']}?rev={cur['_rev']}"
        r = req.delete(url, auth=self.db_auth)
        return r.status_code == 200
    return False

  def update_templated_doc(self, database, template, data):
      tpl = env.get_template(template)
      doc = json.loads(tpl.render(data))
      return self.update_doc(database, doc)

  def configure_single_node(self):
    url = f"{self.db_url}/_cluster_setup"
    data = {"action": "enable_single_node", "singlenode": True, "bind_address": "0.0.0.0", "port": 5984}
    r = req.post(url, auth=self.db_auth, json=data) 
    return r.status_code == 201

  def configure_no_reduce_limit(self):
    url = f"{self.db_url}/_node/_local/_config/query_server_config/reduce_limit"
    data=b'"false"'
    r = req.put(url, auth=self.db_auth, data=data) 
    return r.status_code == 200

  def add_user(self, username: str, password: str):
    userpass = {"name": username, "password": password, "roles": [], "type": "user"}
    url = f"{self.db_url}/_users/org.couchdb.user:{username}"
    res = req.put(url, auth=self.db_auth, json=userpass)
    return res.status_code in [200, 201, 421]

  def add_role(self, database: str, members: list[str] = [], admins: list[str] =[]):  
    roles =  {"admins": { "names": admins, "roles": [] }, "members": { "names": members, "roles": [] } }
    url = f"{self.db_base}{database}/_security"
    res = req.put(url, auth=self.db_auth, json=roles)
    return res.status_code in [200, 201, 421]

#
# Submit a POST request to the _find endpoint using the specified selector
#
  def find_doc(self, database, selector, user=None, password="", no_auth=False):
    url = f"{self.db_base}{database}/_find"
    headers = {'Content-Type': 'application/json'}

    if no_auth:
      db_auth=None
    elif user:
      db_auth=req.auth.HTTPBasicAuth(user, password)
    else:
      db_auth = self.db_auth
    r = req.post(url, auth=db_auth, headers=headers, data=selector)
    if r.status_code == 200:
      return json.loads(r.text)
    
    logging.warn(f"query to {url} failed with {r.status_code}. Body {r.text}")
    return None    

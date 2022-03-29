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
import os, json, time
import requests as req

db_protocol   = os.environ.get("DB_PROTOCOL", "http")
db_prefix     = os.environ.get("DB_PREFIX", "nuvolaris_") 
db_host       = os.environ.get("DB_HOST", "localhost")

db_username   = os.environ.get("COUCHDB_USER",  "whisk_admin")
db_password   = os.environ.get("COUCHDB_PASSWORD", "some_passw0rd")
db_port       = os.environ.get("DB_PORT", "5984")

db_auth = req.auth.HTTPBasicAuth(db_username,db_password)
db_url = f"{db_protocol}://{db_host}:{db_port}"
db_base = f"{db_url}/{db_prefix}"

def wait_db_ready(max_seconds):
    start = time.time()
    while time.time() - start < max_seconds*60:
      try:
        r = req.get(f"{db_url}/_utils", timeout=1)
        if r.status_code == 200:
          return True
        print(r.status_code)
      except:
        print(".", end='')
        pass
    return False

# check if database exists, return boolean
def check_db(database):
  global db_auth, db_base
  url = f"{db_base}{database}"
  r = req.head(url, auth=db_auth)
  return r.status_code == 200
 
# delete database, return true if ok
def delete_db(database):
  global db_auth, db_base
  url = f"{db_base}{database}"
  r = req.delete(url, auth=db_auth)
  return r.status_code == 200

# create db, return true if ok
def create_db(database):
  global db_auth, db_base
  url = f"{db_base}{database}"
  r = req.put(url, auth=db_auth) 
  return r.status_code == 201

# database="subjects"
def recreate_db(database, recreate=False):
  msg = "recreate_db:"
  exists = check_db(database)
  if recreate and exists:
    msg += " deleted"
    delete_db(database)
  if recreate or not exists:
    msg += " created"
    create_db(database)
  return msg

def get_doc(database, id, db_auth=db_auth, db_base=db_base):
  url = f"{db_base}{database}/{id}"
  r = req.get(url, auth=db_auth) 
  if r.status_code == 200:
    return json.loads(r.text)
  return None

def update_doc(database, doc):
  global db_auth, db_base
  if '_id' in doc:
    url = f"{db_base}{database}/{doc['_id']}"
    cur = get_doc(database, doc['_id'])
    if cur and '_rev' in cur:
      doc['_rev'] = cur['_rev']
      r = req.put(url, auth=db_auth, json=doc)
    else:
      r = req.put(url, auth=db_auth, json=doc)
    return r.status_code in [200,201]
  return False

def delete_doc(database, id):
  global db_auth, db_base
  cur = get_doc(database, id)
  if cur and '_rev' in cur:
      url = f"{db_base}{database}/{cur['_id']}?rev={cur['_rev']}"
      r = req.delete(url, auth=db_auth)
      return r.status_code == 200
  return False

from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader(["./nuvolaris/templates", "./nuvolaris/files"])
env = Environment(loader=loader)

def update_templated_doc(database, template, data):
    tpl = env.get_template(template)
    doc = json.loads(tpl.render(data))
    return update_doc(database, doc)



def configure_single_node():
  global db_auth, db_url
  url = f"{db_url}/_cluster_setup"
  data = {"action": "enable_single_node", "singlenode": True, "bind_address": "0.0.0.0", "port": 5984}
  r = req.post(url, auth=db_auth, json=data) 
  return r.status_code == 201

def configure_no_reduce_limit():
  global db_auth, db_url
  url = f"{db_url}/_node/_local/_config/query_server_config/reduce_limit"
  data=b'"false"'
  r = req.put(url, auth=db_auth, data=data) 
  return r.status_code == 200

def add_user(username: str, password: str):
  global db_auth, db_url
  userpass = {"name": username, "password": password, "roles": [], "type": "user"}
  url = f"{db_url}/_users/org.couchdb.user:{username}"
  res = req.put(url, auth=db_auth, json=userpass)
  return res.status_code in [200, 201, 421]

def add_role(database: str, members: list[str] = [], admins: list[str] =[]):  
  global db_auth, db_base
  roles =  {"admins": { "names": admins, "roles": [] }, "members": { "names": members, "roles": [] } }
  url = f"{db_base}{database}/_security"
  res = req.put(url, auth=db_auth, json=roles)
  return res.status_code in [200, 201, 421]


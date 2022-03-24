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
import os, json
import requests as req
from jinja2 import Environment, FileSystemLoader

db_protocol   = os.environ.get("DB_PROTOCOL", "http")
db_prefix     = os.environ.get("DB_PREFIX", "nuvolaris_") 
db_host       = os.environ.get("DB_HOST", "localhost")

db_username   = os.environ.get("COUCHDB_USER",  "whisk_admin")
db_password   = os.environ.get("COUCHDB_PASSWORD", "some_passw0rd")
db_port       = os.environ.get("DB_PORT", "5984")

db_auth = req.auth.HTTPBasicAuth(db_username,db_password)
db_base = f"{db_protocol}://{db_host}:{db_port}/{db_prefix}"

loader = FileSystemLoader(["./nuvolaris/templates", "./nuvolaris/files"])
env = Environment(loader=loader)



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


def test_db():
    """
    >>> from nuvolaris.couchdb_util import *
    >>> check_db("subjects")
    False
    >>> create_db("subjects")
    True
    >>> check_db("subjects")
    True
    >>> create_db("subjects")
    False
    >>> delete_db("subjects")
    True
    >>> delete_db("subjects")
    False
    >>> check_db("subjects")
    False
    >>> recreate_db("subjects")
    'recreate_db: created'
    >>> check_db("subjects")
    True
    >>> recreate_db("subjects")
    'recreate_db:'
    >>> recreate_db("subjects", recreate=True)
    'recreate_db: deleted created'
    >>> delete_db("subjects")
    True
    """
    pass

def get_doc(database, id):
  global db_auth, db_base
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

def delete_doc(database, doc):
  global db_auth, db_base
  if '_id' in doc:
    cur = get_doc(database, doc['_id'])
    if cur and '_rev' in cur:
      url = f"{db_base}{database}/{cur['_id']}?rev={cur['_rev']}"
      r = req.delete(url, auth=db_auth)
      return r.status_code == 200
    return False
  return False
 

def test_doc():
  """
  >>> from nuvolaris.couchdb_util import *
  >>> create_db("subjects")
  True
  >>> db = "subjects"
  >>> get_doc(db, "test") == None
  True
  >>> doc = {"_id":"test", "value":"hello" }
  >>> update_doc(db,  doc)
  True
  >>> get_doc(db, "test")['value']  
  'hello'
  >>> doc['value'] = 'world'
  >>> update_doc(db,  doc)
  True
  >>> get_doc(db, "test")['value']  
  'world'
  >>> delete_doc(db, doc)
  True
  >>> delete_doc(db, doc)
  False
  >>> delete_db("subjects")
  True

  """
  pass

# database = "subjects"
# template = "test.json"
# data = {"item": {"value": {"user": "mic", "pass": "pw"}}}
# data = {"item": "hello"}
def update_template(database, template, data):
    """
    """
    tpl = env.get_template(template)
    doc = json.loads(tpl.render(data))
    res = update_doc(database, doc)

def init(secrets):
  print("SAMPLE EXPAND")
  [ [username, password] ] = list(secrets["couchdb"].items())
  print(sample_expand(username=username, password=password))
  # implement here orig/initdb.yml
  print("SAMPLE REQUEST", sample_request())

if __name__ == "__main__":
  import yaml
  secrets = yaml.safe_load(open("tests/operator-obj.yaml"))["spec"]
  init(secrets)

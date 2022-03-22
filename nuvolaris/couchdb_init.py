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
import os
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
  """
  >>> from nuvolaris.couchdb_init import *
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
  msg = "recreate_db:"
  exists = check_db(database)
  if recreate and exists:
    msg += " deleted"
    delete_db(database)
  if recreate or not exists:
    msg += " created"
    create_db(database)
  return msg


def sample_expand(username, password):
  return env.get_template("createUser.json").render(item={
    "value": {
      "user": username,
      "pass": password 
    }
  })

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

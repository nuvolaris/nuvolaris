import os
import requests as req
from jinja2 import Environment, FileSystemLoader

db_protocol   = os.environ.get("DB_PROTOCOL", "http")
db_prefix     = os.environ.get("DB_PREFIX", "test_") 
db_host       = os.environ.get("DB_HOST", "localhost")
db_username   = os.environ.get("COUCHDB_USER",  "whisk_admin")
db_password   = os.environ.get("COUCHDB_PASSWORD", "some_passw0rd")
db_port       = os.environ.get("DB_PORT", "5984")
db_prefix     = "nuvolaris_"

db_base = f"{db_protocol}://{db_username}:{db_password}@{db_host}:{db_port}/"
db_auth = f"{db_base}{db_prefix}subjects"

loader = FileSystemLoader(["./nuvolaris/templates", "./nuvolaris/files"])
env = Environment(loader=loader)

def user(username, password):
    user = env.get_template("user.json")
    return user.render(item={"value":{"user":username, "pass":password}})
 
def permission():
    permission = env.get_template("permission.json")
    return """
      {
        "admins": {
          "names": [ "{{ adminList | join('", "') }}" ],
          "roles": []
        },
        "members": {
          "names": [ "{{ readerList | union(writerList) | join('", "') }}" ],
          "roles": []
        }
      }
     """


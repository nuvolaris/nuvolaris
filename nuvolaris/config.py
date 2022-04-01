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
import flatdict, json

_config = None
_name = None


# define a configuration singleton with a name
# update to the configurations should retain that name
# delete the configuration
def configure(name: str, spec: dict, labels: list = []):
    global _config, _name
    if _config:
        if name != _name:
            return False
    _name = name
    _config = dict(flatdict.FlatDict(spec, delimiter="."))

    for i in labels:
        for j in list(i.keys()):
            if j.startswith("nuvolaris-"):
                _config[ j[10:] ] = i[j]

    return True

def clean():
    _config = None
    _name = None

def get(key):
    if _config:
        return _config.get(key)
    return None

def put(key, value):
    if _config:
        _config[key] = value
        return True
    return False

def getall(prefix=""):
    res = {}
    if _config:
        for key in _config.keys():
            if key.startswith(prefix):
                res[key] = _config[key]
    return res

def keys(prefix=""):
    res = []
    if _config:
        for key in _config.keys():
            if key.startswith(prefix):
                res.append(key)
    return res

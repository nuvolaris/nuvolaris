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
import os.path
import nuvolaris.kustomize as nku

@kopf.on.login()
def whisk_login(**kwargs):
    token = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    if os.path.isfile(token):
        return kopf.login_via_pykube(**kwargs)
    return kopf.login_via_client(**kwargs)

@kopf.on.create('whisks')
def whisk_create(spec, **kwargs):
    # TODO: pass from configurations somewhere
    print("whisk_create")
    TAG = "neo-21.1230.16"
    IMG = "ghcr.io/nuvolaris/openwhisk-standalone"
    yaml = nku.kustomize("openwhisk-standalone", nku.image(IMG, newTag=TAG))
    print(yaml)
    return {'message': 'created'}


@kopf.on.delete('whisks')
def whisk_delete(spec, **kwargs):
    print("whisk_delete")
    return {'message': 'deleted'}


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
import nuvolaris.kustomize as nku
import nuvolaris.kube as kube
import kopf
import os, os.path
import logging

# tested by an integration test
@kopf.on.login()
def whisk_login(**kwargs):
    token = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    if os.path.isfile(token):
        logging.debug("found serviceaccount token: login via pykube in kubernetes")
        return kopf.login_via_pykube(**kwargs)
    logging.debug("login via client")
    return kopf.login_via_client(**kwargs)

# tested by an integration test
@kopf.on.create('nuvolaris.org', 'v1', 'whisks')
def whisk_create(spec, **kwargs):
    IMG = os.environ.get("STANDALONE_IMAGE", "ghcr.io/nuvolaris/openwhisk-standalone")
    TAG = os.environ.get("STANDALONE_TAG", "latest")
    logging.debug("whisk_create: %s:%s" % (IMG,TAG) )
    spec = nku.kustom_list("openwhisk-standalone", nku.image(IMG, newTag=TAG))
    kopf.adopt(spec)
    logging.debug(spec)
    kube.apply(spec)
    return {'message': 'created'}

# tested by an integration test
@kopf.on.delete('nuvolaris.org', 'v1', 'whisks')
def whisk_delete(spec, **kwargs):
    print("whisk_delete")
    return {'message': 'deleted'}

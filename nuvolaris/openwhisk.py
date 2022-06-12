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
import nuvolaris.kustomize as kus
import nuvolaris.kube as kube
import nuvolaris.config as cfg
import os, os.path
import urllib.parse
import logging
import kopf

CONTROLLER_SPEC = "state.controller.spec"

# this functtions returns the apihost to be stored as annotation
def apihost(apiHost):
    url = urllib.parse.urlparse("https://pending")
    if len(apiHost) > 0: 
        if "hostname" in apiHost[0]:
            url = url._replace(netloc = apiHost[0]['hostname'])
        elif "ip" in apiHost[0]:
            url = url._replace(netloc = apiHost[0]['ip'])

    if cfg.exists("nuvolaris.apihost"):
        url =  url._replace(netloc = cfg.get("nuvolaris.apihost"))
    if cfg.exists("nuvolaris.protocol"):
        url = url._replace(scheme = cfg.get("nuvolaris.protocol"))
    if cfg.exists("nuvolaris.apiport"):
        url = url._replace(netloc = f"{url.hostname}:{cfg.get('nuvolaris.apiport')}")
    return url.geturl()

def create(owner=None):
    data = {
        "couchdb_host": cfg.get("couchdb.host", "COUCHDB_SERVICE_HOST", "couchdb"),
        "couchdb_port": cfg.get("couchdb.port", "COUCHDB_SERVICE_PORT", "5984"),
        "admin_user": cfg.get("couchdb.admin.user"),
        "admin_password": cfg.get("couchdb.admin.password"),
        "triggers_fires_perMinute": cfg.get("openwhisk.limits.triggers.fires-perMinute"),
        "actions_sequence_maxLength": cfg.get("openwhisk.limits.actions.sequence-maxLength"),
        "actions_invokes_perMinute": cfg.get("openwhisk.limits.actions.invokes-perMinute"),
        "actions_invokes_concurrent": cfg.get("openwhisk.limits.actions.invokes-concurrent")
    }
    whisk_image = cfg.get("controller.image") or  "missing-controller-image"
    whisk_tag = cfg.get("controller.tag") or "missing-controller-tag"
    config = kus.image(whisk_image, newTag=whisk_tag)
    spec = kus.kustom_list("openwhisk-standalone", config, templates=["standalone-kcf.yaml"], data=data)

    if owner:
        kopf.append_owner_reference(spec['items'], owner)
    else:
        cfg.put(CONTROLLER_SPEC, spec)
    return kube.apply(spec)

def delete():
    res = ""
    if cfg.exists(CONTROLLER_SPEC):
        res = kube.delete(cfg.get(CONTROLLER_SPEC))
        cfg.delete(CONTROLLER_SPEC)
    res += kube.kubectl("delete", "pod", "-l", "user-action-pod=true")

def annotate(keyval):
    kube.kubectl("annotate", "cm/config",  keyval, "--overwrite")

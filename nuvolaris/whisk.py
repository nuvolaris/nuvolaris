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
import os, os.path
import logging

WHISK_IMG = os.environ.get("STANDALONE_IMAGE", "ghcr.io/nuvolaris/openwhisk-standalone")
WHISK_TAG = os.environ.get("STANDALONE_TAG", "latest")

def whisk_create():
    spec = nku.kustom_list("openwhisk-standalone", nku.image(WHISK_IMG, newTag=WHISK_TAG))
    #kopf.adopt(spec)
    #logging.debug(spec)
    return kube.apply(spec)


def whisk_delete():
    spec = nku.kustom_list("openwhisk-standalone", nku.image(WHISK_IMG, newTag=WHISK_TAG))
    return kube.apply(spec)

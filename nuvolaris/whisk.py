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
import urllib.parse

WHISK_IMG = os.environ.get("STANDALONE_IMAGE", "ghcr.io/nuvolaris/openwhisk-standalone")
WHISK_TAG = os.environ.get("STANDALONE_TAG", "latest")

# this functtions returns
def apihost(apiHost, nodeLabels):
    """
    >>> a = []
    >>> l =  [ {"beta.kubernetes.io/arch": "arm64", "nuvolaris-apihost": "localhost", "nuvolaris-apiport": "3233", "nuvolaris-protocol": "http"} ]
    >>> whisk_apihost(a,l)
    http://localhost:3233
    >>> a = [ { "hostname": "elb.amazonaws.com"} ]
    >>> l = []
    >>> whisk_apihost(a, l)
    http://elb.amazonaws.com
    >>> a = [ { "hostname": "elb.amazonaws.com"} ]
    >>> l =  [ { "nuvolaris-apiport": "3233", "nuvolaris-protocol": "https"} ]
    >>> whisk_apihost(a, l)
    https://elb.amazonaws.com:3233
    """
    url = urllib.parse.urlparse("http://localhost")
    if len(apiHost) > 0 and "hostname" in apiHost[0]:
        url = url._replace(netloc = apiHost[0]['hostname'])

    for node in nodeLabels:
        if "nuvolaris-apihost" in node:
            url =  url._replace(netloc = node["nuvolaris-apihost"])
        if "nuvolaris-protocol" in node:
            url = url._replace(scheme = node["nuvolaris-protocol"])
        if "nuvolaris-apiport" in node:
            url = url._replace(netloc = url.hostname+":"+node["nuvolaris-apiport"])

    return url.geturl()


def create():
    spec = nku.kustom_list("openwhisk-standalone", nku.image(WHISK_IMG, newTag=WHISK_TAG))
    info = kube.apply(spec)
    logging.debug(info)    
    return "created whisk"

def delete():
    spec = nku.kustom_list("openwhisk-standalone", nku.image(WHISK_IMG, newTag=WHISK_TAG))
    info = kube.delete(spec)
    logging.debug(info)
    return "deleted whisk"

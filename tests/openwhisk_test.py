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

import nuvolaris.config as cfg
import nuvolaris.testutil as tu
import nuvolaris.openwhisk as ow
import nuvolaris.kube as kube
import os

# apihost
assert(cfg.configure(tu.load_sample_config(), clean=True))
assert(ow.apihost([]) == "https://pending")

cfg.put("nuvolaris.apihost", "localhost")
assert(ow.apihost([]) == 'https://localhost')

cfg.put("nuvolaris.protocol", "http")
cfg.put("nuvolaris.apiport", "3232")
assert( ow.apihost([]) == 'http://localhost:3232')

a = [ { "hostname": "elb.amazonaws.com"} ]
assert( ow.apihost(a) == 'http://localhost:3232')
assert(cfg.configure(tu.load_sample_config(), clean=True))
assert( ow.apihost(a) == 'https://elb.amazonaws.com')

import doctest
doctest.testfile("tests/openwhisk_test.txt", module_relative=False)

!kubectl apply -f deploy/nuvolaris-operator/nuvolaris-common.yaml
!kubectl apply -f deploy/nuvolaris-operator/whisk-crd.yaml
!kubectl apply -f tests/whisk-dev.yaml

wsk = kube.get("wsk/controller")
ow.create(wsk)

assert(kube.get("deploy/controller"))

!kubectl delete wsk/controller
!kubectl wait wsk/controller --for=delete

assert(not kube.get("deploy/controller"))

ow.delete()




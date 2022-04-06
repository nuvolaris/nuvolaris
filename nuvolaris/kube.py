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
# this module wraps kubectl
import nuvolaris.testutil as tu
import subprocess
import json
import logging
import yaml

output = ""
error = ""
returncode = -1

dry_run = False

mocker = tu.MockKube()

# execute kubectl commands
# default namespace is nuvolaris, you can change with keyword arg namespace
# default output is text
# if you specify jsonpath it will filter and parse the json output
# returns exceptions if errors
def kubectl(*args, namespace="nuvolaris", input=None, jsonpath=None):
    """Test kube
    >>> import nuvolaris.kube as kube, nuvolaris.testutil as tu
    >>> tu.grep(kube.kubectl("get", "ns"), "kube-system", field=0)
    kube-system
    >>> kube.returncode
    0
    >>> "default" in kube.kubectl("get", "ns", jsonpath="{.items[*].metadata.name}")
    True
    >>> tu.catch(lambda: kube.kubectl("error"))
    <class 'Exception'> Error: flags cannot be placed before plugin name: -n
    >>> print(kube.returncode, kube.error.strip())
    1 Error: flags cannot be placed before plugin name: -n
    >>> tu.grep(kube.kubectl("apply", "-f", "-", input=kube.configMap("test", file='Hello')), "configmap")
    configmap/test created
    >>> tu.grep(kube.kubectl("get", "cm/test", "-o", "yaml"), r"name: t|file: H", sort=True)
    file: Hello
    name: test
    >>> tu.grep(kube.kubectl("delete", "cm/test"), "configmap")
    configmap "test" deleted
    """

    # support for mocked requests
    mres = mocker.invoke(*args)
    if mres:
        mocker.save(input)
        return mres

    cmd = ["kubectl", "-n", namespace]
    cmd += list(args)
    if jsonpath:
        cmd += ["-o", "jsonpath-as-json=%s" % jsonpath]

    # if is a string, convert input in bytes
    try: input = input.encode('utf-8')
    except: pass
        
    # executing
    logging.debug(cmd)
    res = subprocess.run(cmd, capture_output=True, input=input)

    global returncode, output, error
    returncode = res.returncode
    output = res.stdout.decode()
    error = res.stderr.decode()

    if res.returncode == 0:
        if jsonpath:
                parsed = json.loads(output)
                logging.debug("result: %s", json.dumps(parsed, indent=2))
                return parsed
        else:
            return output
    raise Exception(error)

# create a configmap from keyword arguments
def configMap(name, **kwargs):
    """
    >>> import nuvolaris.kube as kube, nuvolaris.testutil as tu
    >>> tu.grep(kube.configMap("hello", value="world"), "kind:|name:|value:", sort=True)
    kind: ConfigMap
    name: hello
    value: world
    >>> tu.grep(kube.configMap("hello", **{"file.js":"function", "file.py": "def"}), "file.", sort=True)
    file.js: function
    file.py: def
    """
    out = yaml.safe_load("""apiVersion: v1
kind: ConfigMap
metadata:
  name: %s
data: {}
"""% name)
    for key, value in kwargs.items():
        out['data'][key] = value
    return yaml.dump(out)
    
# delete an object
def delete(obj, namespace="nuvolaris"):
    # tested with apply
    if not isinstance(obj, str):
        obj = json.dumps(obj)
    return kubectl("delete", "-f", "-", namespace=namespace, input=obj)

# apply an object
def apply(obj, namespace="nuvolaris"):
    """
    >>> import nuvolaris.kube as kube, nuvolaris.testutil as tu, nuvolaris.kustomize as nku
    >>> obj = {"apiVersion": "v1", "kind": "Namespace", "metadata":{"name":"nuvolaris"}}
    >>> _ = kube.apply(obj)
    >>> print(kube.apply(obj).strip())
    namespace/nuvolaris unchanged
    >>> obj = nku.kustom_list("test")
    >>> print(kube.apply(obj).strip())
    service/test-svc created
    pod/test-pod created
    >>> print(kube.delete(obj).strip())
    service "test-svc" deleted
    pod "test-pod" deleted
    """
    if not isinstance(obj, str):
        obj = json.dumps(obj)
    return kubectl("apply", "-f", "-", namespace=namespace, input=obj)

# patch an object
def patch(name, data, namespace="nuvolaris", tpe="merge"):
    """
    >>> from nuvolaris.testutil import nprint
    >>> nprint(kubectl("apply", "-f", "deploy/test/_crd.yaml"))
    customresourcedefinition.apiextensions.k8s.io/samples.nuvolaris.org created
    >>> nprint(kubectl("apply", "-f", "deploy/test/_obj.yaml"))
    sample.nuvolaris.org/obj created
    >>> nprint(kubectl("get", "sample/obj"))
    NAME   MESSAGE
    obj    
    >>> nprint(patch("sample/obj", {"spec": {"message": "hello"}}))
    sample.nuvolaris.org/obj patched
    >>> nprint(kubectl("get", "sample/obj"))
    NAME   MESSAGE
    obj    hello
    >>> nprint(kubectl("delete", "-f", "deploy/test/_obj.yaml"))
    sample.nuvolaris.org "obj" deleted
    >>> nprint(kubectl("delete", "-f", "deploy/test/_crd.yaml"))
    customresourcedefinition.apiextensions.k8s.io "samples.nuvolaris.org" deleted
    """
    if not type(data) == str:
        data = json.dumps(data)
    res = kubectl("patch", name, "--type", tpe, "-p", data)
    return res
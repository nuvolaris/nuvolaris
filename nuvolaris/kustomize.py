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
# this module wraps generation of kustomizations

import os, io, yaml
import nuvolaris.kube as kube
import nuvolaris.kustomize as nku
import nuvolaris.template as ntp

# execute the kustomization of a folder under "deploy"
# sperficied with `where`
# it generate a kustomization.yaml, adding the header 
# then including all the files of that folder as resources
# you have to pass a list of kustomizations to apply
# you can use various helpers in this module to generate customizations
# it returns the expanded kustomization
def kustomize(where, *what):
    """Test kustomize
    >>> import nuvolaris.kustomize as ku
    >>> import nuvolaris.testutil as tu
    >>> tu.grep(ku.kustomize("test", ku.image("nginx", "busybox")), "kind|image:", sort=True)
    - image: busybox
    kind: Pod
    kind: Service
    >>> tu.grep(ku.kustomize("test", configMapTemplate("test-cm", "test", "test.json", {"item":"value"})), r"_id|value")
    "_id": "test",
    "value": "value"
    """
    # prepare the kustomization
    dir = f"deploy/{where}"
    tgt = f"{dir}/kustomization.yaml"
    with open(tgt, "w") as f:
        f.write("apiVersion: kustomize.config.k8s.io/v1beta1\nkind: Kustomization\n")
        for s in list(what):
            f.write(s)
        f.write("resources:\n")
        dirs = os.listdir(f"deploy/{where}")
        dirs.sort()
        for file in dirs:
            if file == "kustomization.yaml":
              continue
            if file.startswith("_"):
              continue
            f.write(f"- {file}\n")
    return kube.kubectl("kustomize", dir)

# generate image kustomization
def image(name, newName=None, newTag=None):
    """Test image
    >>> import nuvolaris.kustomize as ku
    >>> print(ku.image("busybox"), end='')
    images:
    - name: busybox
    >>> print(ku.image("busybox", "nginx"), end='')
    images:
    - name: busybox
      newName: nginx
    >>> print(ku.image("busybox", newTag="nightly"), end='')
    images:
    - name: busybox
      newTag: nightly
    >>> print(ku.image("busybox", "nginx", "nightly"), end='')
    images:
    - name: busybox
      newName: nginx
      newTag: nightly
    """
    r = f"images:\n- name: {name}\n"
    if newName: r += f"  newName: {newName}\n"
    if newTag:  r += f"  newTag: {newTag}\n"
    return r

# generate a configmap kustomization expanding a template
def configMapTemplate(name, where, template, data):
    """   
    >>> import nuvolaris.testutil as tu
    >>> print(configMapTemplate("test-cm", "test", "test.json", {"item":"value"}), end='')
    configMapGenerator:
    - name: test-cm
      files:
      - test.json=_test.json
    """
    out = f"deploy/{where}/_{template}"
    file = ntp.spool_template(template, out, data)
    return f"""configMapGenerator:
- name: {name}
  files:
  - {template}=_{template}
"""

def secretLiteral(name, *args):
  """
  >>> import nuvolaris.testutil as tu
  >>> import nuvolaris.kustomize as ku
  >>> tu.grep(ku.secretLiteral("test-sec", "user=mike", "pass=hello"), r"name:|user=|pass=")
  - name: test-sec
  - user=mike
  - pass=hello
  """
  res = f"""secretGenerator:
- name: {name}
  namespace: nuvolaris
  literals:
"""
  for arg in args:
    res += f"   - {arg}\n"
  return res

# returns a list of kustomized objects
def kustom_list(where, *what):
  """
  >>> import nuvolaris.kustomize as nku
  >>> where = "test"
  >>> what = []
  >>> res = nku.kustom_list(where, *what)
  >>> out = [x['kind'] for x in res['items']]
  >>> out.sort()
  >>> print(out)
  ['Pod', 'Service']
  """
  yml = nku.kustomize(where, *what)
  stream = io.StringIO(yml)
  res = list(yaml.load_all(stream, yaml.Loader))
  return {"apiVersion": "v1", "kind": "List", "items": res }

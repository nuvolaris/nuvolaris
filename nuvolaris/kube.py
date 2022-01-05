#import logging, importlib as imp
#logging.basicConfig(level=logging.DEBUG)
#import nuvolaris.kube as kube
#imp.reload(kube)
#imp.reload(tu)

import subprocess
import nuvolaris.testutil as testutil
import os
import json
import logging

mode = "apply"
output = ""
error = ""
returncode = -1

# execute kubectl commands
# default namespace is nuvolaris, you can change with keyword arg namespace
# default output is text
# if you specify jsonpath it will filter and parse the json output
# returns exceptions if errors
def kubectl(*args, namespace="nuvolaris", jsonpath=None):
    """
    imp.reload(kube)
    imp.reload(tu)
    >>> import nuvolaris.kube as kube
    >>> import nuvolaris.testutil as tu
    >>> tu.grep(kube.kubectl("get", "ns"), "kube-system", field=0)
    kube-system
    >>> kube.returncode
    0
    >>> "default" in kube.kubectl("get", "ns", jsonpath="{.items[*].metadata.name}")
    True
    >>> tu.catch(lambda: kube.kubectl("error"))
    <class 'Exception'> Error: flags cannot be placed before plugin name: -n
    >>> kube.returncode, kube.error
    (1, 'Error: flags cannot be placed before plugin name: -n\n')
    """
    cmd = ["kubectl", "-n", namespace] 
    cmd += list(args)
    if jsonpath:
        cmd += ["-o", "jsonpath-as-json=%s" % jsonpath] 
    logging.debug("command: %s", " ".join(cmd))
    # executing
    res = subprocess.run(cmd, capture_output=True)

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
    

# execute the kustomization of a folder under "deploy"
# uses the mode variable to decide if kustomize, apply or delete
# it generate a kustomization.yaml, adding the header 
# then including all the files of a folder as resources
# so you do not have to specify them
# returns True or False, 
# if True, check output for stdout and error for stderrs
# if False, check error 
def kustomize(where, what):
    global mode, output, error
    # prepare the kustomization
    tgt = f"deploy/{where}/kustomization.yaml"
    with open(tgt, "w") as f:
        f.write("apiVersion: kustomize.config.k8s.io/v1beta1\nkind: Kustomization\n")
        f.write(what)
        f.write("resources:\n")
        for file in os.listdir(f"deploy/{where}"):
            if file != "kustomization.yaml":
                f.write(f"- {file}\n")
    
    # generate command
    cmd = ["kubectl"]
    if mode == "kustomize":
        cmd.append("kustomize")
    elif mode == "delete":
        cmd += ["delete", "-k"]
    elif mode == "apply":
        cmd += ["apply", "-k"]
    else:
        error = "kustomize.mode should be kustomize, delete or apply"
        return False
    cmd.append(f"deploy/{where}")
    logging.debug(cmd)

    # execute it
    res = subprocess.run(cmd, capture_output=True)
    logging.debug(res)
    output = res.stdout.decode()
    error = res.stderr.decode()
    return res.returncode == 0




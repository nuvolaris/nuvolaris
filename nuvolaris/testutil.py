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
import yaml
import re


# takes a string, split in lines and search for the word (a re)
# if field is a number, splits the line in fields separated by spaces and print the selected field
# the output is always space trimmed for easier check
def grep(input, word, field=None, sort=False):
    r"""
    >>> import nuvolaris.testutil as tu
    >>> tu.grep("a\nb\nc\n", "b")
    b
    >>> tu.grep(b"a\nb\n c\n", r"a|c")
    a
    c
    >>> tu.grep(b"z\nt\n w\n", r"w|z", sort=True)
    w
    z
    """
    try: input = input.decode()
    except: pass
    lines = []
    for line in str(input).split("\n"):
        if re.search(word, line):
            line = line.strip()
            if not field is None:
                try:
                    line = line.split()[field]
                except:
                    line = "missing-field"
            lines.append(line)
    if sort:
        lines.sort()
    print("\n".join(lines))


# print a file
def cat(file):
    with open(file, "r") as f:
        print(f.read())

# print a file
def fread(file):
    with open(file, "r") as f:
        return f.read()


# capture and print an exception with its type
# or just print the output of the fuction
def catch(f):
    """
    >>> import nuvolaris.testutil as tu
    >>> tu.catch(lambda: "ok")
    ok
    >>> def error():
    ...   raise Exception("error")
    >>> tu.catch(error)
    <class 'Exception'> error
    """
    try: print(f().strip())
    except Exception as e:
        print(type(e), str(e).strip())

# print not blank lines only
def nprint(out):
    for line in out.split("\n"):
        if line.strip() != "":
            print(line)

# load an YAML file
def load_yaml(file):
    f = open(file)
    l = list(yaml.load_all(f, yaml.Loader))
    if len(l)  > 0:
        return l[0]
    return {}

# mocking and spying kube support
class MockKube:
    """
    >>> from nuvolaris.testutil import *
    >>> m = MockKube()
    >>> m.invoke()
    >>> m.config("", "ok")
    >>> m.invoke()
    'ok'
    >>> m = MockKube()
    >>> m.config("apply", "applied")
    >>> m.invoke()
    >>> m.echo()
    >>> m.invoke("apply", "-f")
    kubectl apply -f
    'applied'
    >>> m.peek()
    kubectl apply -f
    'apply -f'
    >>> m.dump()
    ''
    >>> m.save("hello")
    >>> m.dump()
    'hello'
    """ 
    def __init__(self):
        self.reset()

    def reset(self):
        self.map = {}
        self.queue = []
        self.saved = []
        self.echoFlag = False
        self.enabled = False

    def echo(self, flag=True):
        self.echoFlag = flag

    def peek(self, index=-1):
        res = self.queue[index][0]
        print("kubectl", res)
        return res

    def dump(self, index=-1):
        return self.queue[index][1]

    def save(self, data, index=-1):
        self.queue[index] = (self.queue[index][0], data)

    def config(self, request, response):
        self.enabled = True
        self.map[request] = response

    def invoke(self, *args):
        if self.enabled:
            cmd = " ".join(args)
            for key in list(self.map.keys()):
                if cmd.startswith(key):
                    if self.echoFlag:
                        print("kubectl", cmd)
                    self.queue.append( (cmd,"") )
                    return self.map[key]
        return None

def load_sample_config(suffix=""):
    with open(f"deploy/nuvolaris-operator/whisk{suffix}.yaml") as f: 
        c = yaml.safe_load(f)
        name = f"{c['metadata']['namespace']}:{c['metadata']['name']}"
        return (name, c['spec'])

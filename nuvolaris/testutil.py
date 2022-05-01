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
import yaml
import re
import flatdict
import json
import time

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
    res = "\n".join(lines)
    print(res)


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

def load_sample_config(name="whisk"):
    with open(f"tests/{name}.yaml") as f: 
        c = yaml.safe_load(f)
        return c['spec']

def json2flatdict(data):
    return dict(flatdict.FlatterDict(json.loads(data), delimiter="."))

def get_by_key_sub(dic, key):
    res = []
    for k in list(dic.keys()):
        try:
            k.index(key)
            res.append(dic[k])
        except:
            pass
    return "\n".join(res)

def read_dotenv():
    import os
    try:
        f = open(".env")
        lines = f.readlines()
        #print(lines)
        for line in lines:
            #print(line)
            #line = lines[1]
            a = line.split("=", 1)
            if len(a) == 2:
                print(a[0])
                os.environ[a[0]] = a[1].strip()
        f.close()
    except Exception as e:
        print(e)
        print(".env not found")
        pass

def get_with_retry(url, max_seconds):
    start = time.time()
    delta = 0
    while delta < max_seconds:
        try:
            r = req.get(url, timeout=1)
            print(r)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            #print(e)
            print(f"waiting since: {delta} seconds")
        delta = int(time.time() - start)
        time.sleep(1)
    return ""

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
import re


# takes a string, split in lines and search for the word (a re)
# if field is a number, splits the line in fields separated by spaces and print the selected field
# the output is always space trimmed for easier check


def grep(input, word, field=None):
  r"""Test grep

  >>> import nuvolaris.testutil as tu
  >>> tu.grep("a\nb\nc\n", "b")
  b
  >>> tu.grep(b"a\nb\n c\n", r"a|c")
  a
  c
  """
  try: input = input.decode()
  except: pass
  for line in input.split("\n"):
    if re.search(word, line):
        line = line.strip()
        if not field is None:
            try:
                line = line.split()[field]
            except:
                line = "missing-field"
        print(line)

# capture and print an excection
def catch(f):
    try: f()
    except Exception as e:
        print(type(e), str(e).strip())

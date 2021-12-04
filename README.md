<!--
  ~ Licensed to the Apache Software Foundation (ASF) under one
  ~ or more contributor license agreements.  See the NOTICE file
  ~ distributed with this work for additional information
  ~ regarding copyright ownership.  The ASF licenses this file
  ~ to you under the Apache License, Version 2.0 (the
  ~ "License"); you may not use this file except in compliance
  ~ with the License.  You may obtain a copy of the License at
  ~
  ~   http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing,
  ~ software distributed under the License is distributed on an
  ~ "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  ~ KIND, either express or implied.  See the License for the
  ~ specific language governing permissions and limitations
  ~ under the License.
  ~
-->
# nuvolaris-operator
This repo builds our operator and published the image in the GitHub docker registry.

You can discuss it in the #[nuvolaris-operator](https://discord.gg/RzJ4FHR2aR) discord channel and in the forum under the category [operator](https://github.com/nuvolaris/nuvolaris/discussions/categories/operator).

**Work in progress - this stuff is incomplete and unstable.**

## Install and Run

To use it in current state (whatever it is!):

- Get an Unix environment (Linux/OSX/Windows+WSL)
- Install Python3
- bash setup.sh to initialize
- bash run.sh to run

## References

This operator is built in Python with [kopf](https://kopf.readthedocs.io/en/stable/).

You can find some [examples here](https://github.com/nolar/kopf/tree/main/examples).


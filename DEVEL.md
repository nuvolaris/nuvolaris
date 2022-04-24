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
# Developer Guide

Random notes that helps understanding the code.

Principles:

- you start and test writing a YAML configuration 
- you modifify the yaml using kustomize
- there are python wrappers to generate all the kustomizations
- the operator react to events and execute kustomizations

Testing:

Multiple level of testings

- you first test algorithm with unit tests (`task unit` - I use a lot doctest
- you then test with integration tests without starting the operator (`task integ`) - tests uses ipython and assertions
- you can run the operator locally without deploying it (with `task dev:run`) and run task `test:*` commands against it
- you can then deploy in local kind and execute tests (`task test:all`) 
- finally you test built the image and publish it with `task image-tag ; git push --tags`, wait it builds and test against real kubernetes

Debugging:

- I use dev:cli to launch ipython with autoreload
- I use control-enter and control-shift-enter to send code to the cli



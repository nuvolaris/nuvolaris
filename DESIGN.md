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
# Design Document

The operator is built with `kopf`. It is basically a server that will react to events coming from Kubernetes. The main evento to react to is the deployment of a Custom Resource Definition that configures OpenWhisk and all the related components.

All the code is in the package `nuvolaris`.  Events are handled in `main.py`.

Each event handlers uses utility functions you can find the various service specific files like `openwhisk` or `couchdb`.

Each function is implemented


## Developmnet Targets


The operator will control Kubernetes either using locally configured `kubeconfig`, or within Kubernetes itself using the configuration files that Kubernetes makes available.

You should start the operator with `test run` that will initialize the environment so the operator can connect to the current configured Kubernetes and control it. You can also interact on the CLI and execute the code using `task cli`.

## Development Workflow 

In generale the operator react to events and execute kustomizations.
To develop, 
- you start and test writing a base YAML configuration in code. 
- you can then modify this base configuration in code using `kustomize` (wrapped in python)
- finally you apply the configuration with `kubectl` (wapped in python)
  


# Testing:

Multiple level of testings

- you first test algorithm with unit tests (`task unit` - I use a lot doctest
- you then test with integration tests without starting the operator (`task integ`) - tests uses ipython and assertions
- you can run the operator locally without deploying it (with `task dev:run`) and run task `test:*` commands against it
- you can then deploy in local kind and execute tests (`task test:all`) 
- finally you test built the image and publish it with `task image-tag ; git push --tags`, wait it builds and test against real kubernetes

Debugging:

- I use dev:cli to launch ipython with autoreload
- I use control-enter and control-shift-enter to send code to the cli



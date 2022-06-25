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

## Development Workflow 

In generale the operator react to events and execute kustomizations.
To develop, 
- you start and test writing a base YAML configuration in code. 
- you can then modify this base configuration in code using `kustomize` (wrapped in python)
- finally you apply the configuration with `kubectl` (wapped in python)

A good example of how to build a configuration is the following

You start creating a basic definition under `deploy` for example `couchdb`. All the utils searches set of deployments under some folder under `deploy`. 

Then you can do this (obvious details omitted)

```
1    kust =  kus.secretLiteral("couchdb-auth", user, pasw)
2    kust += kus.patchTemplate("couchdb", "set-attach.yaml", data) 
3    spec = kus.kustom_list("couchdb", kust, templates=["couchdb-init.yaml"], data=data)
4    kube.apply(spec)

```

In `1` you create a customization to create a secret. 

In `2` there is a customization to create a `patch` for it. There are a few utility functions for that in the `nuvolaris.kustomize` package. Some of them are actually templatized (have Template name) so the actual file is generated expanding a template. All the templates are under `nuvolaris/templates`.  A templatized configuration uses `Jinja2`. When you use templates you also have to provide the `data` dictionary for the templates.

3. Once you finisced you generate a configuration to be applied. Usually it is better to be a series of configuration, hence you invoke `kustom_list`. Note that kustom list, in addition to customize a configuration, can also add more configuration in the form of templates. Specificy the templates to use as `templates=templates` and do not forget to provide `data=data` to provide data

4. Finally you apply the configuration with `kube.apply` - there are more utility functions running `kubectl` in a pythonic way.

# Testing

There are multiple level of testings

- you first test algorithm with unit tests (`task utest` - I use a lot doctest)
- you then test with integration tests without starting the operator (`task itest`) - tests uses ipython and assertions
- you can run the operator locally without deploying it (with `task run`) and run task `deploy` to deploy a test CRD.
- you can then deploy in local kind with `task build-and-load` without having to publish it, then  execute tests (see the TaskfileTest.yml)
- finally you test built the image and publish it with `task image-tag ; git push --tags`, wait it builds and test against real kubernetes, using the Taskfle


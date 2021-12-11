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

This is the Kubernetes Operator of the [bit.ly/nuvolaris](nuvolaris project). Follow the link to learn more.

You can discuss it in the #[nuvolaris-operator](https://discord.gg/RzJ4FHR2aR) discord channel and in the forum under the category [operator](https://github.com/nuvolaris/nuvolaris/discussions/categories/operator).

## Developer Guide

Instructions to use this repository.

## Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) on Mac or Windows, or  [Docker Engine](https://docs.docker.com/engine/install/) on Linux.
- Get a Kubernetes that you can access with `kubectl`. If you use Docker Desktop, the simplest way is to enable it as it is includes. On Linux you can create a test cluster with [Kind](https://kind.sigs.k8s.io/).
- Install [VSCode](https://code.visualstudio.com/) and the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
- Fork `nuvolaris-operator` in your github accou,t
- Open the repository in a volume with `F1` | `Remote-Containers: Clone Repositories in a Container Volume` then log in GitHub and select your fork.
- Now, from the external, copy your Kubernetes configuration inside the container with:

```
docker cp \$HOME/.kube/config nuvolaris-controller:/etc/kubeconfig
```

## Setup 

- Open a termina in the container and type:

```
source setup.source
```

You are ready to develop!





*TODO* Instructions to 

## References

This operator is built in Python with [kopf](https://kopf.readthedocs.io/en/stable/).

You can find some [examples here](https://github.com/nolar/kopf/tree/main/examples).


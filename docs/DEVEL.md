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

This document describes development procedures.

You can use either:

- [Use VSCode and the prebuilt Devcontainer](#use-vscode-and-the-prebuilt-devcontainer) that is the easiest and faster way to work, but you need to use VSCode and a Linux-based environment

- [Build your own development environment](#build-your-own-development-environment) so you can use your IDE and tools, but the setup is up to you and we provide only generic instructions

## Use VSCode and the prebuilt Devcontainers 

Using this option you can directly work and develop a single subproject. For example `nuvolaris-operator`.

**The instructions are the same for the others `nuvolaris-*` subprojects, of course change to `nuvolaris-cli` for the CLI, etc**

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) on Mac or Windows, or  [Docker Engine](https://docs.docker.com/engine/install/) on Linux.
- Get a Kubernetes that you can access with `kubectl`. If you use Docker Desktop, the simplest way is to enable it as it is includes. On Linux you can create a test cluster with [Kind](https://kind.sigs.k8s.io/).
- Install [VSCode](https://code.visualstudio.com/) and the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
- Fork your subproject (for example `nuvolaris-operator`) in your github account

Now you can either:

- Open the repository in a volume with `F1` | `Remote-Containers: Clone Repositories in a Container Volume` then log in GitHub and select your fork.
- Now, from your desktop, open a terminal, change to your home directory and copy your Kubernetes configuration inside the container with: `docker cp .kube/config nuvolaris-controller:/etc/kubeconfig` 

Or:

- Clone a module repository in your local filesystem
- Copy the `.kube/config` from your home directory to the folder where you cloned the repository as `kubeconfig`
- Open the folder with VSCode. It will ask you if you want to reopen it in the container. Say yes.

Once you are running in the container, oppen a terminal in VSCode and type:

```
source setup.source
```

## Example

For example, if you want to develop the operator using an OSX/Linux environment you can do from the command line:

```
git clone https://github.com/nuvolaris/nuvolaris-operator
cd nuvolaris-operator
cp $HOME/.kube/config kubeconfig
code .
```

Open the terminal and type: `source setup.source`

You are ready to develop!

## Build your own development environment

If you do not want to use our choices and containers you can setup your own development environment. 

Development happens in **modern** Unix-like environments. So you need either Mac OSX, a Linux distribution or Windows with WSL.

You need to preinstall:

- [Linux Development tools](#linux-development-tools)
- [Java JDK](#java-jdk) v11 or later
- [Docker and Kubernetes](#docker-and-kubernetes) 

Then run [setup script] we provide.

### Java JDK
For Java, we test with [Amazon Corretto](https://docs.aws.amazon.com/corretto/index.html), but very likely can use any other Java distribution.

### Linux Development Tools

Procedures to install development tools:

- OSX: `xcode-select --install`
- Debian or Ubuntu: `sudo apt-get install build-essential procps curl file git`
- Fedora, CentOS, or Red Hat: `sudo yum groupinstall 'Development Tools' && sudo yum install procps-ng curl file git`

### Docker and Kubernetes

You need to [install Docker](https://docs.docker.com/get-docker/) and enable Kubernetes for it.

If you are using Docker Desktop you need to enable Kubernetes. If you are using a Linux based environment you can install a Kubernetes environment with [kind](https://kind.sigs.k8s.io/).

### Setup Script

Once the prerequisites are satisfied you can build the actual development environment with:


```
git clone --recurse-submodules https://github.com/nuvolaris/nuvolaris
cd nuvolaris
source setup.source
```

This will setup all the common components.

You can then change to each subfolder, read the README and if there is one, run the module specific `setup.source` 

For example:

- `cd operator ; source setup.source`
- `cd cli ; source setup.source`
- `cd admim ; source setup.source`

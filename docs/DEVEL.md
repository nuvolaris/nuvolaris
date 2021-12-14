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

This document describes development procedures for Nuvolaris.

You can use either:

- [Use VSCode and the prebuilt Devcontainer](#use-vscode-and-the-prebuilt-devcontainer) that is the easiest and faster way to work, but you need to use VSCode and work in a Linux-based environment in a container with `bash`.

- [Build your own development environment](#build-your-own-development-environment) so you can use your IDE and tools, but the setup is up to you and we provide only generic instructions.

## Use VSCode and the prebuilt Devcontainers 

Using this option you can directly work and develop each subproject in a development containers with all the dependencies already installed.

Before starting development, you need to: 

- Install [VSCode](https://code.visualstudio.com/) 
- Install the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
- Fork one of the [nuvolaris subprojects](https://github.com/nuvolaris/nuvolaris) in your account, the clone the fork in your local filesystem
- [Setup a development Kubernetes cluster](#setup-a-development-kubernetes-cluster)

The recommended procedure for development then is:

- Copy the `.kube/config` from your home directory to the folder where you cloned the repository as `kubeconfig`
- Open the folder with VSCode. It will ask you if you want to reopen it in the container. Say yes.
- Once you are running in the container, open a terminal in VSCode and you are ready.

Note that accessing to code in your local filesystem can be slow. In alternative you can put code in a docker volume with this alternative procedure:

- Start VSCode
- Open the repository in a volume with `F1` | `Remote-Containers: Clone Repositories in a Container Volume` 
- Log in GitHub and select your fork.
- Now, from your desktop, open a terminal, change to your home directory and copy your Kubernetes configuration inside the container with: `docker cp .kube/config nuvolaris-controller:/etc/kubeconfig` 

## Build your own development environment

If you do not want to use VSCode andcontainers you can setup your own development environment. Here we provide generic instructions, your mileage may vary.

Developent happens in **modern** Unix-like environments. So you need either Mac OSX, a Linux distribution or Windows with WSL. Working with non-unix environment can be possible but it can turn out to be difficult.

Before starting you need to preinstall:

- [System Development tools](#system-development-tools)
- [Java JDK](#java-jdk) v11 or later
- [Docker and Kubernetes](#setup-a-development-kubernetes-cluster) 

Then clone everything with

```
git clone --recurse-submodules https://github.com/nuvolaris/nuvolaris
```

Once you have all of this you can start development with

```
cd nuvolaris
bash --init-script setup.source
```

Note that it will take a long time only the first time to dowloand and install the used tools. 


### Java JDK

For Java, we test with [Amazon Corretto](https://docs.aws.amazon.com/corretto/index.html).

You should be able however to use other devent Java distribution.

### System Development Tools

Procedures to install development tools:

- OSX: `xcode-select --install`
- Debian or Ubuntu: `sudo apt-get install build-essential procps curl file git`
- Fedora, CentOS, or Red Hat: `sudo yum groupinstall 'Development Tools' && sudo yum install procps-ng curl file git`

## Setup a development Kubernetes cluster

For development you need a Kubernetes cluster. You can get one from various sources in cloud, or setup a local one.

We currently test with two local environments: [Docker Desktop Kubernetes](https://www.docker.com/products/kubernetes) on Mac and Linux, and [kind](https://kind.sigs.k8s.io/) on Linux.

To use Docker Desktop Kubernetes, just enable it on [Windows](https://docs.docker.com/desktop/windows/#kubernetes) or [Mac](https://docs.docker.com/desktop/mac/#kubernetes).

To use Kind, just follow [Installation instructions](https://kind.sigs.k8s.io/docs/user/quick-start/)

You end up with a configuration file stored in your home directory, under `.kube/config` that you can copy inside your source code folder or in the running container as described before, or use directly.
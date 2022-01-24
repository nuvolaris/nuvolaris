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

This document describes the evelopment procedures for Nuvolaris.

## Prerequisites

Before starting you need a computer with enough memory. Since we use extensively Docker and create a local development environemnt, you need t [install docker](https://docs.docker.com/get-docker/) either on Windows, OSX or Linux and **assign to Docker at least 8 gb of memory**. 

Given the high memory footprinr required, it is pretty unlikely you can work productively on any machine with less than 12G of memory. 

You can then either:

- [Use VSCode and the prebuilt Devcontainer](#use-vscode-and-the-prebuilt-devcontainer) that is the easiest and faster way to work, but you need to use VSCode and work in a Linux-based environment in a container with `bash`.

- [Build your own development environment](#build-your-own-development-environment) so you can use your IDE and tools, but the setup is up to you and we provide only generic instructions.

## Use VSCode and the prebuilt devcontainer

Using this option you can directly work and develop each subproject in a development containers with all the dependencies already installed.

Before starting development, you need to: 

- Install [VSCode](https://code.visualstudio.com/) 
- Install the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
- Fork one of the [nuvolaris subprojects](https://github.com/nuvolaris/nuvolaris) in your account, the clone the fork in your local filesystem
- Open the folder with VSCode and then say YES when it asks to "reopen in container"
- Finally, open the workspace (the file `workspace.code-workspace`) present in every subproject.

Note that accessing to code stored in your local filesystem can be slow. In alternative you can put code in a docker volume with this alternative procedure:

- Start VSCode
- Open the repository in a volume with `F1` | `Remote-Containers: Clone Repositories in a Container Volume` 
- Log in GitHub and select your fork.
- Open your workspace.

## Build your own development environment

If you do not want to use VSCode and our development container, you can setup your own development environment. Here we provide generic instructions, your mileage may vary.

Developent happens in **modern** Unix-like environments. So you need either Mac OSX, a Linux distribution or Windows with WSL. Working with non-unix environment (like Windows PowerShell) can be possible but it can turn out to be difficult. We do not support it, you are on your own.

Before starting you need to preinstall:

- [System Development tools](#system-development-tools)
- [Java JDK](#java-jdk) v11 or later
- [Docker](#setup-a-development-kubernetes-cluster) 

Then clone everything with

```
git clone --recurse-submodules https://github.com/nuvolaris/nuvolaris
```

Once you have all of this you can start development with

```
cd nuvolaris
./init.sh # once
./start.sh # every time
```

Note that it will take a long time only the first time to dowloand and install the used tools. It will also create a local Kubernetes cluster using Kind.


### Java JDK

For Java, we test with [Amazon Corretto](https://docs.aws.amazon.com/corretto/index.html).

You should be able however to use other Java distribution.

### System Development Tools

Procedures to install development tools:

- OSX: `xcode-select --install`
- Debian or Ubuntu: `sudo apt-get install build-essential procps curl file git`
- Fedora, CentOS, or Red Hat: `sudo yum groupinstall 'Development Tools' && sudo yum install procps-ng curl file git`


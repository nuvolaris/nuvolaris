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

This document describes the development procedures for Nuvolaris.

## Prerequisites

Before starting you need a computer with enough memory. Since we use extensively Docker and create a local development environemnt, you need to [install docker](https://docs.docker.com/get-docker/) either on Windows, OSX or Linux and **assign to Docker at least 6 gb of memory**. 

The version of Docker we currently use and we have tested is **20.x**, either Docker Desktop or Docker CE. Earlier version may work or not work. Definitely the `docker.io` distributed with Ubuntu *does not work* and you have to update to Docker-CE.

Given the high memory footprinr required, it is pretty unlikely you can work productively on any machine with less than 16G of memory. 

either:

- [Use VSCode and the prebuilt Development Container](#use-vscode-and-the-prebuilt-devcontainer). That is the easiest and faster way to work, but you need to use VSCode and work in a Linux-based environment in a container with `bash`.

- [Use VSCode and the prebuilt Devcontainer on a Remote Server](#use-vscode-and-the-prebuilt-devcontainer-on-a-remote-server) for who doesn't have enough RAM to work on his machine, or simply prefer to use a remote server for development.

- [Build your own development environment](#build-your-own-development-environment) so you can use your IDE and tools, but the setup is up to you and we provide only generic instructions.

## Use VSCode and the prebuilt devcontainer

Using this option you can directly work and develop each subproject in a development containers with all the dependencies already installed.

Before starting development, you need to: 

- Install [VSCode](https://code.visualstudio.com/), at least version 1.16.x
- Install the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
- Now you can clone all the source code with `git clone --recurse-submodules https://github.com/nuvolaris/nuvolaris`
- Open the folder with VSCode and then say YES when it asks to "reopen in container"
- Finally, open one of the workspace file (the file `workspace.code-workspace`) present in every subproject in the folders `nuvolaris-*`

Accessing to code stored in your local filesystem can be slow. Also you may have other problems, especially with Linux if the user you are using has an uid != 1000, since this is the uid used internally by the container.

As an alternative you can put code in a docker volume with this alternative procedure, that works for the various `nuvolaris-*` subprojects, but not for the top-level `nuvolaris` project as it uses submodules (not yet supported by VSCode).

- Fork one of the Nuvolaris repository in your account. 
- Start VSCode
- Open the repository in a volume with `F1` | `Remote-Containers: Clone Repositories in a Container Volume` 
- Log in GitHub and select your fork.
- Open your workspace.

## Use VSCode and the prebuilt Devcontainer on a Remote Server

This option is very similar to the one [before](#use-vscode-and-the-prebuilt-devcontainer), the only real difference is that Docker, the code and the dependencies will be on the remote server, only VScode will be on your machine.

On the Linux-based remote server you need to:
- [Install docker](https://docs.docker.com/get-docker/)
- clone all the source code with 'git clone --recurse-submodules https://github.com/nuvolaris/nuvolaris'

On your machine:
- Install [VSCode](https://code.visualstudio.com/) 
- Install the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
- Install the [Remote - SSH](https://code.visualstudio.com/docs/remote/ssh-tutorial#_connect-using-ssh) extension.

When everything is installed:
- Use the remote SSH extension to [connect to the Remote Server](https://code.visualstudio.com/docs/remote/ssh-tutorial#_connect-using-ssh)
- Open the folder with VSCode and then say YES when it asks to "reopen in container"
- Finally, open one of the workspace file (the file workspace.code-workspace) present in every subproject in the folders nuvolaris-*

## Use a virtual machine

You can build a virtual machine which has all the required components starting a virtual machine with `Ubuntu 22` in any cloud provider and feed to them the `cloud-init.yaml` in the nuvolaris folder.

If you have [multipass](https://multipass.dev) you can also directly start a suitable VM using the `multipass.sh` script to launch and initialize it. Then connect to it as it was a remote server.

If you use a virtual machine created with cloud-init you do not need to launch the development container as it has already all the required tools.

## Build your own development environment

If you do not want to use VSCode and our development container, you can setup your own development environment. Here we provide generic instructions, your mileage may vary.

Developent happens in **modern** Unix-like environments. So you need either Mac OSX, a Linux distribution or Windows with WSL. Working with non-unix environment (like Windows PowerShell) can be possible but it can turn out to be difficult. We do not support it, you are on your own.

Before starting you need to preinstall:

- [System Development tools](#system-development-tools)
- [Java JDK](#java-jdk) v8 or later
- Docker Desktop or CE, version 20.x or later

Then clone everything with:

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

Procedures to install Unix development tools (also valid in the various Windows WSL distributions):

- OSX: `xcode-select --install`
- Debian or Ubuntu: `sudo apt-get install build-essential procps curl file git`
- Fedora, CentOS, or Red Hat: `sudo yum groupinstall 'Development Tools' && sudo yum install procps-ng curl file git`

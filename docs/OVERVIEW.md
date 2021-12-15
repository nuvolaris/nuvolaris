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
# Index

- [Overview](#overview)
- Repo [`nuvolaris`](#nuvolaris-controller)
- Repo [`nuvolaris-controller`](#nuvolaris-controller)
- Repo [`nuvolaris-runtimes`](#nuvolaris-runtimes)
- Repo [`nuvolaris-operator`](#nuvolaris-operator)
- Repo [`nuvolaris-cli`](#nuvolaris-cli)
- Repo [`nuvolaris-config`](#nuvolaris-config)
- Repo [`nuvolaris-testing`](#nuvolaris-testing)
- Repo [`nuvolaris-training`](#nuvolaris-training)

## Overview

In this diagrama there is an overview of the repos in the Nuvolaris organization:

![nuvolaris](./nuvolaris.png)

The main repositories, those relevant for the project, are  pinned and named `nuvolaris-*`.   All the other, especially those starting with `openwhisk*` and `nimbella*` are forks of our upstream source code. 

If we to make changes to our fork, we try to limit changes to the absolute minimum. 

Our work is always placed in branches starting with `nuvolaris`, and then they are included as git modules in the main ones.  And we try, when possible, to contribute back our changes tp upstream.

Development procedures are described in the [DEVEL](./DEVEL.md) document.

[Up.](#index)

### [`nuvolaris`](https://github.com/nuvolaris/nuvolaris)

This repo is the starting point.

It contains:

- project management documentation (that you are reading right now)
- the build for the development environment container
- references to all the other repositories
- the [Discussion Forum](https://github.com/nuvolaris/nuvolaris/discussions)
- the [Issue Tracker](https://github.com/nuvolaris/nuvolaris/issues) to manage the whole project.

To discuss the project in general, introduce yourself, make suggestions or ask questions, post in the [general]  category on forum or join the  the  #[general](https://discord.gg/VSGG7aQ2Ds) discord and ask.

[Up.](#index)

### [`nuvolaris-controller`](https://github.com/nuvolaris/nuvolaris-controller)

This repo builds the OpenWhisk controller that is the core of OpenWhisk and publishes the images in the GitHub docker registry.

It includes as a subrepo our fork of [apache/openwhisk](https://github.com/nuvolaris/openwhisk)

You can discuss it in the #[nuvolaris-controller](https://discord.gg/2weUATjvV7) discord channel and in the forum under the category [controller](https://github.com/nuvolaris/nuvolaris/discussions/categories/controller).

[Up.](#index)

### [`nuvolaris-runtimes`](https://github.com/nuvolaris/nuvolaris-runtimes)

This repo builds the OpenWhisk runtimes and publishes the images in the GitHub docker registry.

It includes as a subrepo our fork of some (but not all) `apache/openwhisk-runtime-*`

You can discuss it in the #[nuvolaris-runtimes](https://discord.gg/ZPZZYMG4pS) discord channel and in the forum under the category [runtimes](https://github.com/nuvolaris/nuvolaris/discussions/categories/runtimes).

[Up.](#index)

### [`nuvolaris-operator`](https://github.com/nuvolaris/nuvolaris-operator)

This repo builds our operator and published the image in the GitHub docker registry.

You can discuss it in the #[nuvolaris-operator](https://discord.gg/RzJ4FHR2aR) discord channel and in the forum under the category [operator](https://github.com/nuvolaris/nuvolaris/discussions/categories/operator).

### [`nuvolaris-cli`](https://github.com/nuvolaris/nuvolaris-cli)

This repo builds our operator and published the image in the GitHub docker registry.

You can discuss it in the #[nuvolaris-cli](https://discord.gg/JWqFJJfvED) discord channel and in the forum under the category [operator](https://github.com/nuvolaris/nuvolaris/discussions/categories/cli).

[Up.](#index)

# nuvolaris-config

This repo includes the configurator of the operator.

You can discuss it in the #[nuvolaris-config](https://discord.gg/TfhXXxqXzj) discord channel and in the forum under the category [config](https://github.com/nuvolaris/nuvolaris/discussions/categories/config).

[Up.](#index)

### [`nuvolaris-testing`](https://github.com/nuvolaris/nuvolaris-testing)

This repo includes our test suite and the scripts to build our test environments.

You can discuss it in the #[nuvolaris-testing](https://discord.gg/sgXqn9we) discord channel and in the forum under the category [testing](https://github.com/nuvolaris/nuvolaris/discussions/categories/testing).

[Up.](#index)

### [`nuvolaris-training`](https://github.com/nuvolaris/nuvolaris-training)

This repo includes training material.

You can discuss it in the #[nuvolaris-training](https://discord.gg/TeNA2Pa5Nu) discord channel and in the forum under the category [training](https://github.com/nuvolaris/nuvolaris/discussions/categories/training).

[Up.](#index)

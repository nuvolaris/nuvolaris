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
# Nuvolaris

Welcome to Nuvolaris. Starting points:

- Chat with us on [Discord](https://discord.gg/VSGG7aQ2Ds)
- Discuss with us on [Forum](https://github.com/nuvolaris/nuvolaris/discussions/)
- Read our [Roadmap](docs/ROADMAP.md).

## About

This is an ongoing project, that is still in early stages, to build an Open Source distribution of [Apache OpenWhisk](https://openwhisk.apache.org) licensed released under the [Apache Licence 2.0](LICENSE) (like OpenWhisk itself)

Before you ask, I tell you that there are currently no releases yet. So if you look for something to run, you are out of luck. If you look for contributing to an Open Source project, then maybe you can find something of interest.

## Index

- [About this project](#about-this-project)
- [Get in touch](#get-in-touch)
- [What is the next activity?](#what-is-the-next-activity)
- [How to contribute](#how-to-contribute)
- [Overview of the project](#overview-of-the-project)
- Repo [`nuvolaris`](#nuvolaris-controller)
- Repo [`nuvolaris-controller`](#nuvolaris-controller)
- Repo [`nuvolaris-runtimes`](#nuvolaris-runtimes)
- Repo [`nuvolaris-operator`](#nuvolaris-operator)
- Repo [`nuvolaris-cli`](#nuvolaris-cli)
- Repo [`nuvolaris-admin`](#nuvolaris-admin)
- Repo [`nuvolaris-testing`](#nuvolaris-testing)
- Repo [`nuvolaris-training`](#nuvolaris-training)

##  About this project

We want to build a *complete* distribution of a serverless environment that is:

- it is easy to install and manage
- potentially runs in every Kubernetes, but it works on a tested set
- includes a good set of integrated services

THis is the main differentiation from Apache OpenWHisk as it only provides a basic engine for serverless.

Our goals are described in our [**roadmap**](docs/ROADMAP.md) document to read about.

[Up.](#index)

## Get in touch

Do you want to help?

- Start [introducing yourself in the forum](https://github.com/nuvolaris/nuvolaris/discussions/7) and partecipating to discussions.
- Chat with us joining our [discord server](https://discord.gg/VSGG7aQ2Ds).   Note there is a channel for every repository in the project to discuss specific issues.

[Up.](#index)

## What is the next activity?

We split activities in milestones. We give to them a friendly name and we name milestones after characters the movies of The Matrix franchise. 

 The  current milestone (the first one) is [Neo](docs/Neo.md). And of course the milestone to reach to release 1.0 is [Matrix](docs/Matrix.md).
 
 Future Milestones will be named Trinity, Morpheus, Smith and so on.

To manage the milestones we use [GitHub Projects](https://github.com/nuvolaris/nuvolaris/projects) that in turn uses  the [GitHub Issue Tracker](https://github.com/nuvolaris/nuvolaris/issues).

[Up.](#index)

## How to contribute

In order to contribute to our project:

- Review the [Code Contribution](docs/CONTRIBUTING.md) rules. In particular we need you sign the [Apache CLA (Contributor License)](http://www.apache.org/licenses/#clas) and include the  [Apache License Header](https://www.apache.org/legal/src-headers.html) in every file. Also every PR will have to pass the existing tests (there are none yet but there will be).
- Either find an open and unassigned issue, or open one by yourself in the [Issue Tracker](https://github.com/nuvolaris/nuvolaris/issues) describing what you want to do.
- Please discuss *in the forum*  and ensure you want to do is approved by the [project owners](OWNERS.md), if you want to be sure your PR will be merged. We can still merge unsolicited PR, but if you do not discuss it before there is some risk that for some reason we may unable to merge it. -
- Get an issue assigned. Seriously. 
- Code it!
- Submit a Pull Request and get it merged after the review.

[Up.](#index)

## Overview of the project

There are lot of repos in this organization. 

The main repositories, those relevant  for the project, are  pinned and named `nuvolaris*`.   All the other, especially those starting with `openwhisk*` and `nimbella*` are forks of our upstream source code. 

If we to make changes to our fork, we try to limit changes to the absolute minimum. Our work is always placed in branches starting with `nuvolaris`, and then they are included as git modules in the main ones.  And we try, when possible, to contribute back our changes tp upstream.

Let's review the main repositories:

[Up.](#index)

### [`nuvolaris`](https://github.com/nuvolaris/nuvolaris)

This repo is the starting point.

It contains:

- project management documentation (that you are reading right now)
- the build for the development environment container
- references to all the other repositories
- the [discussion forum](https://github.com/nuvolaris/nuvolaris/discussions)
- the [Issue Tracker](https://github.com/nuvolaris/nuvolaris/issues) to manage the whole project.

To discuss the project in general, introduce yourself, make suggestions or ask questions, post in the [general]   category on forum or join the  the  #[general](https://discord.gg/VSGG7aQ2Ds) discord and ask.

Do not ask if you can ask, just ask :)

As a prerequisite, you need an modern Unix environment, either Linux, OSX os Windows WSL.
You need to preinstall java and build tools

If you have those you can start with:

```
git clone --recurse-submodules https://github.com/nuvolaris/nuvolaris
cd nuvolaris
source setup.source
```

More details are in the [DEVEL](docs/DEVEL.md) document.

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

# nuvolaris-admin

This repo includes the administrative interface.

You can discuss it in the #[nuvolaris-admin](https://discord.gg/TfhXXxqXzj) discord channel and in the forum under the category [admin](https://github.com/nuvolaris/nuvolaris/discussions/categories/admin).

[Up.](#index)

### [`nuvolaris-testing`](https://github.com/nuvolaris/nuvolaris-testing)

This repo includes our test suite and the scripts to build our test environments.

You can discuss it in the #[nuvolaris-testing](https://discord.gg/sgXqn9we) discord channel and in the forum under the category [testing](https://github.com/nuvolaris/nuvolaris/discussions/categories/testing).

[Up.](#index)

### [`nuvolaris-training`](https://github.com/nuvolaris/nuvolaris-training)

This repo includes training material.

You can discuss it in the #[nuvolaris-training](https://discord.gg/TeNA2Pa5Nu) discord channel and in the forum under the category [training](https://github.com/nuvolaris/nuvolaris/discussions/categories/training).

[Up.](#index)

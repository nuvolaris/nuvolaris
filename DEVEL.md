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

# Prequequisite

Development happens in **modern** Unix-like environments. Basically, we are supporting OSX, Linux and Windows WSL. 

You need to preinstall Java v8 or v11 and C Development tools. Other tools are installed with a script we provide.

And you need to install Docker 

For Java, we use [Amazon Corretto](https://docs.aws.amazon.com/corretto/index.html), but you can use any other Java distribution.

Procedures to install development tools:

- OSX: `xcode-select --install`
- Debian or Ubuntu: `sudo apt-get install build-essential procps curl file git`
- Fedora, CentOS, or Red Hat: `sudo yum groupinstall 'Development Tools' && sudo yum install procps-ng curl file git`

# Checking out and setup

Start with

```
git clone --recurse-submodules https://github.com/nuvolaris/nuvolaris
cd nuvolaris
source setup.source
```

And you are ready!

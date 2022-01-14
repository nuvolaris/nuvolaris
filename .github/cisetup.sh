#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
sudo sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
apt-get update && apt-get -y upgrade
apt-get -y install python3.9 python3.9-venv curl sudo
curl -sSL https://install.python-poetry.org | python3.9 -
WSK_VERSION=1.2.0
WSK_BASE=https://github.com/apache/openwhisk-cli/releases/download
ARCH=amd64
WSK_URL="$WSK_BASE/$WSK_VERSION/OpenWhisk_CLI-$WSK_VERSION-linux-$ARCH.tgz"
curl -sL "$WSK_URL" | tar xzvf - -C ~/.local/bin/

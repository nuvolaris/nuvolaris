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
VERSION="${1:?version}"
EXT="tar.gz"
EXTRACT="tar xzvf"

case "$(arch)" in
  x86_64) ARCH=amd64 ;;
  arm64) ARCH=arm64 ;;
  *) echo "unknown architecture"; exit 1 ;;
esac

case "$(uname)" in
    Darwin) OS="darwin" ;;
    Linux) OS="linux" ;;
    MINGW*)
        OS="windows"
        EXT="zip"
        ARCH="amd64"
        EXTRACT="unzip -o"
    ;;
    *) echo "unknown platform"; exit 1 ;;
esac

URL="https://github.com/nuvolaris/nuvolaris-cli/releases/download/$VERSION/nuv-$VERSION-$OS-$ARCH.$EXT"

curl -sL $URL >dld.$EXT
$EXTRACT "dld.$EXT"

./nuv devcluster destroy
./nuv setup --devcluster

echo 'function main(args) { return { "body": "OK" } }' >ok.js
./nuv action create ok ok.js --web true
URL="$(./nuv url ok)"

if curl -sL $URL | grep OK
then echo "SUCCESS"; exit 0
else echo "FAILED" ; exit 1
fi

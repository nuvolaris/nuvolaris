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
FROM ubuntu:20.04
ENV STANDALONE_IMAGE=ghcr.io/nuvolaris/openwhisk-standalone
ENV STANDALONE_TAG=0.2.0-trinity.22030822
# configure dpkg && timezone
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# install Python
RUN apt-get update && apt-get -y upgrade &&\
    apt-get -y install python3.9 python3.9-venv curl sudo
# Download Kubectl
RUN KVER="v1.23.0" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    KURL="https://dl.k8s.io/release/$KVER/bin/linux/$ARCH/kubectl" ;\
    curl -sL $KURL -o /usr/bin/kubectl && chmod +x /usr/bin/kubectl
# Download WSK
RUN WSK_VERSION=1.2.0 ;\
    WSK_BASE=https://github.com/apache/openwhisk-cli/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    WSK_URL="$WSK_BASE/$WSK_VERSION/OpenWhisk_CLI-$WSK_VERSION-linux-$ARCH.tgz" ;\
    curl -sL "$WSK_URL" | tar xzvf - -C /usr/bin/
# add user
RUN useradd -m -s /bin/bash nuvolaris && \
    echo "nuvolaris ALL=(ALL:ALL) NOPASSWD: ALL" >>/etc/sudoers
WORKDIR /home/nuvolaris
# install the operator
ADD nuvolaris/*.py /home/nuvolaris/nuvolaris/
ADD openwhisk/ansible/files/*.json /home/nuvolaris/openwhisk/ansible/files/
ADD deploy /home/nuvolaris/deploy/
ADD run.sh pyproject.toml poetry.lock /home/nuvolaris/
RUN chown -R nuvolaris:nuvolaris /home/nuvolaris
USER nuvolaris
ENV PATH=/home/nuvolaris/.local/bin:/usr/local/bin:/usr/bin:/sbin:/bin
RUN curl -sSL https://install.python-poetry.org | python3.9 -
RUN cd /home/nuvolaris ; poetry install
CMD ./run.sh

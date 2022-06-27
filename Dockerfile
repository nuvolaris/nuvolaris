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
FROM ubuntu:22.04
ENV CONTROLLER_IMAGE=ghcr.io/nuvolaris/openwhisk-standalone
ENV CONTROLLER_TAG=0.2.1-trinity.22062010
ARG OPERATOR_IMAGE_DEFAULT=ghcr.io/nuvolaris/nuvolaris-operator
ARG OPERATOR_TAG_DEFAULT=0.2.1-trinity.22061708
ENV OPERATOR_IMAGE=${OPERATOR_IMAGE_DEFAULT}
ENV OPERATOR_TAG=${OPERATOR_TAG_DEFAULT}

# configure dpkg && timezone
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# install Python
RUN apt-get update && apt-get -y upgrade &&\
    apt-get -y install apt-utils python3.10 python3.10-venv curl sudo telnet inetutils-ping
# Download Kubectl
RUN KVER="v1.23.0" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    KURL="https://dl.k8s.io/release/$KVER/bin/linux/$ARCH/kubectl" ;\
    curl -sL $KURL -o /usr/bin/kubectl && chmod +x /usr/bin/kubectl
RUN VER="v4.5.4" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2F$VER/kustomize_${VER}_linux_${ARCH}.tar.gz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin
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
ADD nuvolaris/files /home/nuvolaris/nuvolaris/files
ADD nuvolaris/templates /home/nuvolaris/nuvolaris/templates
ADD deploy/nuvolaris-operator /home/nuvolaris/deploy/nuvolaris-operator
ADD deploy/openwhisk-standalone /home/nuvolaris/deploy/openwhisk-standalone
ADD deploy/couchdb /home/nuvolaris/deploy/couchdb
ADD deploy/redis /home/nuvolaris/deploy/redis
ADD run.sh dbinit.sh pyproject.toml poetry.lock /home/nuvolaris/
RUN chown -R nuvolaris:nuvolaris /home/nuvolaris
USER nuvolaris
ENV PATH=/home/nuvolaris/.local/bin:/usr/local/bin:/usr/bin:/sbin:/bin
RUN curl -sSL https://install.python-poetry.org | python3.10 -
RUN cd /home/nuvolaris ; poetry install
CMD ./run.sh

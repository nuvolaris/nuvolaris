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
# configure dpkg && timezone
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# add docker and java (amazon corretto) repos
RUN apt-get update && apt-get -y upgrade &&\
    apt-get -y install curl wget gpg software-properties-common apt-utils unzip
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor > /usr/share/keyrings/docker-archive-keyring.gpg &&\
    wget -O- https://apt.corretto.aws/corretto.key | apt-key add -
RUN ARCH=$(dpkg --print-architecture) ;\
    echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu bionic stable" > /etc/apt/sources.list.d/docker.list &&\
    add-apt-repository 'deb https://apt.corretto.aws stable main'
# install software
RUN apt-get update &&\
 apt-get -y install \
   sudo socat \
   lsb-release \
   build-essential \
   ca-certificates \
   git gnupg curl wget jq \
   zlib1g-dev libbz2-dev libncurses5-dev \
   libgdbm-dev libnss3-dev libssl-dev \
   libreadline-dev libffi-dev libsqlite3-dev \
   java-11-amazon-corretto-jdk \
   docker-ce-cli 
# Download Kubectl
RUN KVER="v1.23.0" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    KURL="https://dl.k8s.io/release/$KVER/bin/linux/$ARCH/kubectl" ;\
    wget $KURL -O /usr/bin/kubectl && chmod +x /usr/bin/kubectl
# Download WSK
RUN WSK_VERSION=1.2.0 ;\
    WSK_BASE=https://github.com/apache/openwhisk-cli/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    WSK_URL="$WSK_BASE/$WSK_VERSION/OpenWhisk_CLI-$WSK_VERSION-linux-$ARCH.tgz" ;\
    curl -sL "$WSK_URL" | tar xzvf - -C /usr/bin/
# Download terraform
RUN ARCH="$(dpkg --print-architecture)" ;\
    TVER=1.1.0 ;\
    TURL="https://releases.hashicorp.com/terraform/$TVER/terraform_${TVER}_linux_${ARCH}.zip" ;\
    curl -sL $TURL -o /tmp/terraform.zip ;\
    unzip /tmp/terraform.zip -d /usr/bin ;\
    rm /tmp/terraform.zip
# setup and initialize the work environment
RUN useradd -m nuvolaris -s /bin/bash &&\
    echo "nuvolaris ALL=(ALL:ALL) NOPASSWD: ALL" >>/etc/sudoers
USER nuvolaris
WORKDIR /home/nuvolaris
ADD setup.source /home/nuvolaris/.bashrc
RUN /bin/bash -c 'source /home/nuvolaris/.bashrc'
# proxy to docker and keep alive
ENTRYPOINT ["/bin/sudo", "/usr/bin/socat", \
  "UNIX-LISTEN:/var/run/docker.sock,fork,mode=660,user=nuvolaris", \
  "UNIX-CONNECT:/var/run/docker-host.sock"]

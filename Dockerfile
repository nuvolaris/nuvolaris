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
FROM ubuntu:20.04 as builder
# download required component
ENV DOCKER_VERSION=18.06.3-ce
ENV WSK_VERSION=1.2.0
ENV DOCKER_BASE=https://download.docker.com/linux/static/stable
ENV WSK_BASE=https://github.com/apache/openwhisk-cli/releases/download
RUN apt-get update && apt-get -y install curl file
RUN DOCKER_URL="$DOCKER_BASE/$(arch)/docker-$DOCKER_VERSION.tgz" ;\
    curl -sL "$DOCKER_URL" | tar xzvf -
RUN ARCH="$(if [[ "$(arch)" == "aarch64" ]] ; then echo "arm64" ; else echo "amd64" ; fi)" ;\
    WSK_URL="$WSK_BASE/$WSK_VERSION/OpenWhisk_CLI-$WSK_VERSION-linux-$ARCH.tgz" ;\
    curl -sL "$WSK_URL" | tar xzvf -
FROM ubuntu:20.04
# configure timezone and configutations
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# add required software packaged
COPY --from=builder /docker/docker /usr/bin/docker
COPY --from=builder /wsk /usr/bin/wsk
RUN apt-get update &&\
 apt-get -y install \
   lsb-release \
   apt-utils \
   software-properties-common \
   build-essential \
   ca-certificates \
   git gnupg curl wget \
   zlib1g-dev libbz2-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev
# add java (amazon corretto)   
RUN wget -O- https://apt.corretto.aws/corretto.key | apt-key add - && \
  add-apt-repository 'deb https://apt.corretto.aws stable main' && \
  apt-get update && \
  apt-get install -y java-11-amazon-corretto-jdk
# setup and initialize the work environment
RUN useradd -m nuvolaris
USER nuvolaris
RUN git clone https://github.com/nuvolaris/nuvolaris /home/nuvolaris/nuvolaris
WORKDIR /home/nuvolaris
RUN /bin/bash -c 'source nuvolaris/setup.source'
RUN echo '. nuvolaris/setup.source' >.bashrc
CMD /bin/bash

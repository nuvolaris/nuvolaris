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
    apt-get -y install curl wget gpg zip unzip software-properties-common apt-utils unzip vim silversearcher-ag
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor > /usr/share/keyrings/docker-archive-keyring.gpg &&\
    wget -O- https://apt.corretto.aws/corretto.key | apt-key add -
RUN ARCH=$(dpkg --print-architecture) ;\
    echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu bionic stable" > /etc/apt/sources.list.d/docker.list &&\
    add-apt-repository 'deb https://apt.corretto.aws stable main'
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" |  tee -a /etc/apt/sources.list.d/google-cloud-sdk.list &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
# install software
RUN apt-get update &&\
    apt-get -y install \
    sudo socat telnet \
    inetutils-ping \
    lsb-release \
    ca-certificates \
    apt-transport-https \
    build-essential gettext-base \
    git gnupg curl wget jq \
    zlib1g-dev libbz2-dev libncurses5-dev \
    libgdbm-dev libnss3-dev libssl-dev \
    libreadline-dev libffi-dev libsqlite3-dev \
    java-11-amazon-corretto-jdk \
    docker-ce-cli \
    google-cloud-cli
# add delta to show diffs
RUN FILE="git-delta_0.11.2_$(dpkg --print-architecture).deb" ;\
    wget "https://github.com/dandavison/delta/releases/download/0.11.2/$FILE" -O "/tmp/$FILE" ;\
    dpkg -i "/tmp/$FILE" ; rm "/tmp/$FILE"
# Download Kubectl
RUN VER="v1.23.0" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://dl.k8s.io/release/$VER/bin/linux/$ARCH/kubectl" ;\
    wget $URL -O /usr/bin/kubectl && chmod +x /usr/bin/kubectl
# Download Kustomize
RUN VER="v4.5.4" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2F$VER/kustomize_${VER}_linux_${ARCH}.tar.gz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin
# Download kind and setup a wrapper
RUN VER="v0.14.0" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/kubernetes-sigs/kind/releases/download/$VER/kind-linux-$ARCH" ;\
    wget $URL -O /usr/bin/kind.bin ;\
    /usr/bin/echo -e '#!/bin/bash\nsudo env DOCKER_HOST=unix:///var/run/docker-host.sock /usr/bin/kind.bin "$@"' >/usr/bin/kind ;\
    chmod +x /usr/bin/kind.bin /usr/bin/kind
# Download terraform
RUN ARCH="$(dpkg --print-architecture)" ;\
    VER=1.1.0 ;\
    URL="https://releases.hashicorp.com/terraform/$VER/terraform_${VER}_linux_${ARCH}.zip" ;\
    curl -sL $URL -o /tmp/terraform.zip ;\
    unzip /tmp/terraform.zip -d /usr/bin ;\
    rm /tmp/terraform.zip
# Add the aws cli and eksctl
RUN mkdir /tmp/awscli ;\
    curl -sL "https://awscli.amazonaws.com/awscli-exe-linux-$(arch).zip" -o "/tmp/awscli/awscliv2.zip" ;\
    cd /tmp/awscli ; unzip awscliv2.zip ;\
    ./aws/install ;\
    rm -Rvf /tmp/awscli
# Install eksctl
RUN curl -sL "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_$(dpkg --print-architecture).tar.gz" |\
    tar xzf - -C /usr/bin
# Install azure cli - commented out: buggy on arm
# RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
# Download openshift installer
RUN VER=4.10.4 ;\
    BASE=https://mirror.openshift.com/pub/openshift-v4/clients/ocp ;\
    ARCH=$(dpkg --print-architecture) ;\
    URL="$BASE/$VER/openshift-install-linux-$VER.tar.gz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin/
# install juju
RUN mkdir /tmp/juju ; cd /tmp/juju ;\
    curl -sL https://launchpad.net/juju/2.9/2.9.0/+download/juju-2.9.0-linux-$(dpkg --print-architecture).tar.xz | tar xJvf - ;\
    install -o root -g root -m 0755 juju /usr/bin/juju ;\
    rm -Rvf /tmp/juju
# Install doctl
RUN DO_VERSION=1.71.0 ;\
    DO_BASE=https://github.com/digitalocean/doctl/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    DO_URL="$DO_BASE/v$DO_VERSION/doctl-$DO_VERSION-linux-$ARCH.tar.gz" ;\
    curl -sL "$DO_URL" | tar xzvf - -C /usr/bin/
# k3sup
RUN VER=0.11.3 ;\
    BASE=https://github.com/alexellis/k3sup/releases/download ;\
    ARCH=-$(dpkg --print-architecture) ;\
    if [[ $ARCH == "amd64" ]] ; then ARCH="" ; fi ;\
    URL="$BASE/$VER/k3sup${ARCH}" ;\
    curl -sL "$URL" >/usr/bin/k3sup ; chmod +x /usr/bin/k3sup
# Download WSK
RUN VER=1.2.0 ;\
    BASE=https://github.com/apache/openwhisk-cli/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    URL="$BASE/$VER/OpenWhisk_CLI-$VER-linux-$ARCH.tgz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin/
# install kn
RUN VER="v1.4.1" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/knative/client/releases/download/knative-$VER/kn-linux-$ARCH" ;\
    curl -sL "$URL" | sudo tee /usr/bin/kn >/dev/null && sudo chmod +x /usr/bin/kn
# Install nuv
RUN VER=v0.2.1 ;\
    BASE=https://github.com/nuvolaris/nuvolaris-cli/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    URL="$BASE/$VER/nuv-$VER-linux-$ARCH.tar.gz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin/
# add and configure user
RUN useradd -m nuvolaris -s /bin/bash &&\
    echo "nuvolaris ALL=(ALL:ALL) NOPASSWD: ALL" >>/etc/sudoers
USER nuvolaris
WORKDIR /home/nuvolaris
# add standard configuations
ADD setup.source /home/nuvolaris/.setup.source
ADD aliases /home/nuvolaris/.aliases
ADD gitconfig /home/nuvolaris/.gitconfig
ADD init.sh /usr/sbin/init.sh
RUN cat .setup.source .aliases >.bashrc ;\
    /bin/bash -c 'source /home/nuvolaris/.bashrc'
# proxy to docker and keep alive
ENTRYPOINT ["/bin/bash", "/usr/sbin/init.sh"]

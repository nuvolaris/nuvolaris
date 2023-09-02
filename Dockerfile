# DO NOT EDIT - edit cloud-init.yaml then regenerate with task dockerfile
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
##BEGIN##
RUN \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN \
    export TZ=Europe/London ; ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN \
    apt-get update && apt-get -y upgrade &&\
    apt-get -y install curl wget gpg zip unzip software-properties-common apt-utils unzip vim silversearcher-ag
RUN \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor > /usr/share/keyrings/docker-archive-keyring.gpg &&\
    wget -O- https://apt.corretto.aws/corretto.key | apt-key add -
RUN \
    ARCH=$(dpkg --print-architecture) ;\
    echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu bionic stable" > /etc/apt/sources.list.d/docker.list &&\
    add-apt-repository 'deb https://apt.corretto.aws stable main'
RUN \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" |  tee -a /etc/apt/sources.list.d/google-cloud-sdk.list &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg >/usr/share/keyrings/cloud.google.gpg
RUN \
    apt-get update &&\
    apt-get -y install \
    sudo socat telnet \
    inetutils-ping \
    lsb-release \
    ca-certificates \
    apt-transport-https \
    build-essential gettext-base \
    git gnupg curl wget jq kafkacat \
    zlib1g-dev libbz2-dev libncurses5-dev \
    libgdbm-dev libnss3-dev libssl-dev \
    libreadline-dev libffi-dev libsqlite3-dev liblzma-dev \
    java-11-amazon-corretto-jdk \
    docker-ce-cli google-cloud-cli
RUN \
    FILE="git-delta_0.11.2_$(dpkg --print-architecture).deb" ;\
    wget "https://github.com/dandavison/delta/releases/download/0.11.2/$FILE" -O "/tmp/$FILE" ;\
    dpkg -i "/tmp/$FILE" ; rm "/tmp/$FILE"
RUN \
    BUILD="0.3.0-dev.2308261806" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    FILE="nuv_$(echo $BUILD)_$ARCH.deb" ;\
    URL="https://github.com/nuvolaris/nuv/releases/download/$BUILD/$FILE" ;\
    rm -Rvf /tmp/nuv-installer ;\
    mkdir /tmp/nuv-installer ;\
    wget $URL -O "/tmp/nuv-installer/$FILE" ;\
    dpkg -i "/tmp/nuv-installer/$FILE"
RUN \
    VER="v1.26.1" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://dl.k8s.io/release/$VER/bin/linux/$ARCH/kubeadm" ;\
    wget $URL -O /usr/bin/kubeadm && chmod +x /usr/bin/kubeadm
RUN \
    VER="v4.5.4" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2F$VER/kustomize_${VER}_linux_${ARCH}.tar.gz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin
RUN \
    ARCH="$(dpkg --print-architecture)" ;\
    VER=1.1.0 ;\
    URL="https://releases.hashicorp.com/terraform/$VER/terraform_${VER}_linux_${ARCH}.zip" ;\
    curl -sL $URL -o /tmp/terraform.zip ;\
    unzip /tmp/terraform.zip -d /usr/bin ;\
    rm /tmp/terraform.zip
RUN \
    mkdir /tmp/awscli ;\
    curl -sL "https://awscli.amazonaws.com/awscli-exe-linux-$(arch).zip" -o "/tmp/awscli/awscliv2.zip" ;\
    cd /tmp/awscli ; unzip awscliv2.zip ;\
    ./aws/install -b /usr/bin  ;\
    rm -Rvf /tmp/awscli
RUN \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash
RUN \
    VER=v0.138.0 ;\
    ARCH="$(dpkg --print-architecture)" ;\
    curl -sL "https://github.com/weaveworks/eksctl/releases/download/${VER}/eksctl_Linux_${ARCH}.tar.gz" |\
    tar xzvf - -C /usr/bin
RUN \
    VER=v3.11.0-rc.2 ;\
    ARCH="$(dpkg --print-architecture)" ;\
    mkdir /tmp/helm ;\    
    curl -sL "https://get.helm.sh/helm-${VER}-linux-${ARCH}.tar.gz" -o "/tmp/helm/helm-${VER}-linux-${ARCH}.tar.gz"; \
    cd /tmp/helm ;\
    tar -zxvf "helm-${VER}-linux-${ARCH}.tar.gz" ;\
    mv "./linux-${ARCH}/helm" /usr/bin/helm ;\
    rm -Rvf /tmp/helm   
RUN \
    VER=4.12.0-0.okd-2023-04-16-041331 ;\
    BASE=https://github.com/okd-project/okd/releases/download ;\
    if dpkg --print-architecture | grep arm64 ;\ 
    then VER1="arm64-$VER" ; else VER1=$VER ; fi ;\
    URL1="$BASE/$VER/openshift-install-linux-$VER1.tar.gz" ;\
    URL2="$BASE/$VER/openshift-client-linux-$VER1.tar.gz" ;\
    curl -sL "$URL1" | tar xzvf - -C /usr/bin/ ;\
    curl -sL "$URL2" | tar xzvf - -C /usr/bin/
RUN \
    mkdir /tmp/juju ; cd /tmp/juju ;\
    curl -sL https://launchpad.net/juju/2.9/2.9.0/+download/juju-2.9.0-linux-$(dpkg --print-architecture).tar.xz | tar xJvf - ;\
    install -o root -g root -m 0755 juju /usr/bin/juju ;\
    rm -Rvf /tmp/juju
RUN \
    DO_VERSION=1.71.0 ;\
    DO_BASE=https://github.com/digitalocean/doctl/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    DO_URL="$DO_BASE/v$DO_VERSION/doctl-$DO_VERSION-linux-$ARCH.tar.gz" ;\
    curl -sL "$DO_URL" | tar xzvf - -C /usr/bin/
RUN \
    ARCH=$(dpkg --print-architecture) ;\
    URL="https://github.com/carvel-dev/ytt/releases/download/v0.40.4/ytt-linux-$ARCH" ;\
    curl -sL "$URL" >/usr/bin/ytt ;\
    chmod +x /usr/bin/ytt
RUN \
    VER="v1.4.1" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/knative/client/releases/download/knative-$VER/kn-linux-$ARCH" ;\
    curl -sL "$URL" | sudo tee /usr/bin/kn >/dev/null && sudo chmod +x /usr/bin/kn
RUN \
    VER=1.2.0 ;\
    BASE=https://github.com/apache/openwhisk-cli/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    URL="$BASE/$VER/OpenWhisk_CLI-$VER-linux-$ARCH.tgz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin/
##END##
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
# add and configure user
RUN VER="v0.14.0" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/kubernetes-sigs/kind/releases/download/$VER/kind-linux-$ARCH" ;\
    wget $URL -O /usr/bin/kind.bin ;\
    /usr/bin/echo -e '#!/bin/bash\nsudo env DOCKER_HOST=unix:///var/run/docker-host.sock /usr/bin/kind.bin "$@"' >/usr/bin/kind ;\
    chmod +x /usr/bin/kind.bin /usr/bin/kind 
ENV TZ=Europe/London
RUN useradd -m nuvolaris -s /bin/bash &&\
    echo "nuvolaris ALL=(ALL:ALL) NOPASSWD: ALL" >>/etc/sudoers
USER nuvolaris
WORKDIR /home/nuvolaris
ADD setup.source /home/nuvolaris/.setup.source
ADD aliases /home/nuvolaris/.aliases
ADD gitconfig /home/nuvolaris/.gitconfig
ADD init.sh /usr/sbin/init.sh
RUN cat .setup.source .aliases >.bashrc ;\
    /bin/bash -c 'source /home/nuvolaris/.bashrc'
# proxy to docker and keep alive
ENTRYPOINT ["/bin/bash", "/usr/sbin/init.sh"]

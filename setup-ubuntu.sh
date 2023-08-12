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

apt-get update && apt-get -y upgrade
apt-get -y install curl wget gpg zip unzip software-properties-common apt-utils unzip vim silversearcher-ag

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor > /usr/share/keyrings/docker-archive-keyring.gpg 
wget -O- https://apt.corretto.aws/corretto.key | apt-key add -

ARCH=$(dpkg --print-architecture)
echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu bionic stable" > /etc/apt/sources.list.d/docker.list 
add-apt-repository 'deb https://apt.corretto.aws stable main'

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" |  tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg >/usr/share/keyrings/cloud.google.gpg

apt-get update 
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
    java-11-amazon-corretto-jdk 
    
FILE="git-delta_0.11.2_$(dpkg --print-architecture).deb" 

wget "https://github.com/dandavison/delta/releases/download/0.11.2/$FILE" -O "/tmp/$FILE" 

dpkg -i "/tmp/$FILE" ; rm "/tmp/$FILE"

VER="v1.26.1" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://dl.k8s.io/release/$VER/bin/linux/$ARCH/kubeadm" ;\
    wget $URL -O /usr/bin/kubeadm && chmod +x /usr/bin/kubeadm

VER="v4.5.4" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2F$VER/kustomize_${VER}_linux_${ARCH}.tar.gz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin

# download the gcloud cli
if ! test -d ~/.local/google-cloud-sdk
then 
    case $(dpkg --print-architecture) in
    (amd64) ARCH=x86_64 ;;
    (arm64) ARCH=arm ;;
    esac
    curl -sL https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-432.0.0-linux-$ARCH.tar.gz | tar xzvf - -C ~/.local
    ~/.local/google-cloud-sdk/install.sh --additional-components gke-gcloud-auth-plugin --quiet
fi
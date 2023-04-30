#!/bin/bash
# DO NOT EDIT - edit cloud-init.yaml then regenerate with task ubuntu
if [[  $(id -u) != "0" ]] ; then echo "please use sudo" ; exit 1 ; fi
##BEGIN##

    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

    export TZ=Europe/London ; ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

    apt-get update && apt-get -y upgrade &&\
    apt-get -y install curl wget gpg zip unzip software-properties-common apt-utils unzip vim silversearcher-ag

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor > /usr/share/keyrings/docker-archive-keyring.gpg &&\
    wget -O- https://apt.corretto.aws/corretto.key | apt-key add -

    ARCH=$(dpkg --print-architecture) ;\
    echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu bionic stable" > /etc/apt/sources.list.d/docker.list &&\
    add-apt-repository 'deb https://apt.corretto.aws stable main'

    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" |  tee -a /etc/apt/sources.list.d/google-cloud-sdk.list &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg >/usr/share/keyrings/cloud.google.gpg

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

    FILE="git-delta_0.11.2_$(dpkg --print-architecture).deb" ;\
    wget "https://github.com/dandavison/delta/releases/download/0.11.2/$FILE" -O "/tmp/$FILE" ;\
    dpkg -i "/tmp/$FILE" ; rm "/tmp/$FILE"

    VER="v1.23.6" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://dl.k8s.io/release/$VER/bin/linux/$ARCH/kubectl" ;\
    wget $URL -O /usr/bin/kubectl && chmod +x /usr/bin/kubectl

    VER="v1.26.1" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://dl.k8s.io/release/$VER/bin/linux/$ARCH/kubeadm" ;\
    wget $URL -O /usr/bin/kubeadm && chmod +x /usr/bin/kubeadm

    VER="v4.5.4" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2F$VER/kustomize_${VER}_linux_${ARCH}.tar.gz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin

    VER="v0.14.0" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/kubernetes-sigs/kind/releases/download/$VER/kind-linux-$ARCH" ;\
    wget $URL -O /usr/bin/kind.bin ;\
    /usr/bin/echo -e '#!/bin/bash\nsudo env DOCKER_HOST=unix:///var/run/docker-host.sock /usr/bin/kind.bin "$@"' >/usr/bin/kind ;\
    chmod +x /usr/bin/kind.bin /usr/bin/kind

    ARCH="$(dpkg --print-architecture)" ;\
    VER=1.1.0 ;\
    URL="https://releases.hashicorp.com/terraform/$VER/terraform_${VER}_linux_${ARCH}.zip" ;\
    curl -sL $URL -o /tmp/terraform.zip ;\
    unzip /tmp/terraform.zip -d /usr/bin ;\
    rm /tmp/terraform.zip

    mkdir /tmp/awscli ;\
    curl -sL "https://awscli.amazonaws.com/awscli-exe-linux-$(arch).zip" -o "/tmp/awscli/awscliv2.zip" ;\
    cd /tmp/awscli ; unzip awscliv2.zip ;\
    ./aws/install -b /usr/bin  ;\
    rm -Rvf /tmp/awscli

    curl -sL https://aka.ms/InstallAzureCLIDeb | bash

    VER=v0.109.0 ;\
    ARCH="$(dpkg --print-architecture)" ;\
    curl -sL "https://github.com/weaveworks/eksctl/releases/download/${VER}/eksctl_Linux_${ARCH}.tar.gz" |\
    tar xzvf - -C /usr/bin

    VER=v3.11.0-rc.2 ;\
    ARCH="$(dpkg --print-architecture)" ;\
    mkdir /tmp/helm ;\    
    curl -sL "https://get.helm.sh/helm-${VER}-linux-${ARCH}.tar.gz" -o "/tmp/helm/helm-${VER}-linux-${ARCH}.tar.gz"; \
    cd /tmp/helm ;\
    tar -zxvf "helm-${VER}-linux-${ARCH}.tar.gz" ;\
    mv "./linux-${ARCH}/helm" /usr/bin/helm ;\
    rm -Rvf /tmp/helm

    ARCH="$(dpkg --print-architecture)" ;\
    MC_VER=RELEASE.2023-03-23T20-03-04Z; \
    rm -Rvf /tmp/minio-binaries ;\
    mkdir /tmp/minio-binaries ;\    
    curl -sL "https://dl.min.io/client/mc/release/linux-${ARCH}/mc.${MC_VER}" --create-dirs -o /tmp/minio-binaries/mc ;\
    chmod +x /tmp/minio-binaries/mc ;\
    mv /tmp/minio-binaries/mc /usr/bin/mc;\
    rm -Rvf /tmp/minio-binaries    

    VER=4.12.0-0.okd-2023-04-16-041331 ;\
    if dpkg --print-architecture | grep arm64 ; then VER="arm64-$VER" ; fi ;\
    BASE=https://github.com/okd-project/okd/releases/download/ ;\
    URL1="$BASE/$VER/openshift-install-linux-$VER.tar.gz" ;\
    URL2="$BASE/$VER/openshift-client-linux-$VER.tar.gz" ;\
    curl -sL "$URL1" | tar xzvf - -C /usr/bin/ ;\
    curl -sL "$URL2" | tar xzvf - -C /usr/bin/

    mkdir /tmp/juju ; cd /tmp/juju ;\
    curl -sL https://launchpad.net/juju/2.9/2.9.0/+download/juju-2.9.0-linux-$(dpkg --print-architecture).tar.xz | tar xJvf - ;\
    install -o root -g root -m 0755 juju /usr/bin/juju ;\
    rm -Rvf /tmp/juju

    DO_VERSION=1.71.0 ;\
    DO_BASE=https://github.com/digitalocean/doctl/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    DO_URL="$DO_BASE/v$DO_VERSION/doctl-$DO_VERSION-linux-$ARCH.tar.gz" ;\
    curl -sL "$DO_URL" | tar xzvf - -C /usr/bin/

    ARCH=$(dpkg --print-architecture) ;\
    URL="https://github.com/carvel-dev/ytt/releases/download/v0.40.4/ytt-linux-$ARCH" ;\
    curl -sL "$URL" >/usr/bin/ytt ;\
    chmod +x /usr/bin/ytt

    VER=0.12.12 ;\
    BASE=https://github.com/alexellis/k3sup/releases/download ;\
    ARCH=-$(dpkg --print-architecture) ;\
    if [[ $ARCH == "amd64" ]] ; then ARCH="" ; fi ;\
    URL="$BASE/$VER/k3sup${ARCH}" ;\
    curl -sL "$URL" >/usr/bin/k3sup ; chmod +x /usr/bin/k3sup

    VER="v1.4.1" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    URL="https://github.com/knative/client/releases/download/knative-$VER/kn-linux-$ARCH" ;\
    curl -sL "$URL" | sudo tee /usr/bin/kn >/dev/null && sudo chmod +x /usr/bin/kn

    VER=1.2.0 ;\
    BASE=https://github.com/apache/openwhisk-cli/releases/download ;\
    ARCH=$(dpkg --print-architecture) ;\
    URL="$BASE/$VER/OpenWhisk_CLI-$VER-linux-$ARCH.tgz" ;\
    curl -sL "$URL" | tar xzvf - -C /usr/bin/
##END##
echo "/home/msciab/nuvolaris/start.sh" >>~/.bashrc

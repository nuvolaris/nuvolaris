#!/bin/bash
[[ $(id -u) == "0" ]] || { echo  "you must be root"; exit 1; }

apt-get update
apt-get -y install git software-properties-common build-essential ca-certificates gnupg lsb-release

# Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get remove docker docker-engine docker.io containerd runc
apt-get -y install docker-ce docker-ce-cli containerd.io

# Install Java
wget -O- https://apt.corretto.aws/corretto.key | sudo apt-key add - 
add-apt-repository 'deb https://apt.corretto.aws stable main'
apt-get update
apt-get install -y java-11-amazon-corretto-jdk

# User
useradd -m nuvolaris
usermod -a nuvolaris -G sudo
usermod -a nuvolaris -G docker
chsh -s /bin/bash nuvolaris

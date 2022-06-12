#!/bin/bash
DNS="${1:?dns}"
sudo microk8s stop
sed -i "/DNS.5/a DNS.6 = $DNS" /var/snap/microk8s/current/certs/csr.conf.template
sudo microk8s start
microk8s config | sed -e "s/server: .*/server: https:\/\/$DNS:16443/" >kubeconfig

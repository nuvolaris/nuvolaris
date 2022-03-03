#!/bin/bash
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
# This script performs initializations, creating a kind clusters
# that works either inside or outside of a container.
#
# check kind is in path
if ! which kind >/dev/null
then echo "Please install Kind from https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
     exit 1
fi

# you are requesting a destroy
if test "$1" == "destroy"
then kind delete clusters nuvolaris
     exit 0
fi

# you are requesting a reset (destroy and recreate)
if test "$1" == "reset"
then kind delete clusters nuvolaris
fi

if test "$1" != ""
then echo "use either no arguments to create a cluster or destroy to destroy it"
    exit 1
fi


# if the nuvolaris cluster already running export its configuration
if kind get clusters | grep nuvolaris >/dev/null 2>/dev/null
then kind export kubeconfig --name nuvolaris
else
  # create cluster
  cat <<EOF | kind create cluster --wait=1m --name=nuvolaris --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
  extraPortMappings:
  - containerPort: 30232
    hostPort: 3232
    protocol: TCP
  - containerPort: 30233
    hostPort: 3233
    protocol: TCP
  - containerPort: 30896
    hostPort: 7896
    protocol: TCP  
EOF
fi

if test -f /.dockerenv
then 
  # copy the kubeconfig
  mkdir -p /home/nuvolaris/.kube 
  sudo cp /root/.kube/config /home/nuvolaris/.kube/config
  sudo chown nuvolaris:nuvolaris /home/nuvolaris/.kube/config
  # proxy to sockerhost and loop forever
  test -S /var/run/docker.sock || exec sudo /usr/bin/socat \
  UNIX-LISTEN:/var/run/docker.sock,fork,mode=660,user=nuvolaris \
  UNIX-CONNECT:/var/run/docker-host.sock
fi

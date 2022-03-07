<!--
  ~ Licensed to the Apache Software Foundation (ASF) under one
  ~ or more contributor license agreements.  See the NOTICE file
  ~ distributed with this work for additional information
  ~ regarding copyright ownership.  The ASF licenses this file
  ~ to you under the Apache License, Version 2.0 (the
  ~ "License"); you may not use this file except in compliance
  ~ with the License.  You may obtain a copy of the License at
  ~
  ~   http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing,
  ~ software distributed under the License is distributed on an
  ~ "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  ~ KIND, either express or implied.  See the License for the
  ~ specific language governing permissions and limitations
  ~ under the License.
  ~
-->
# Manual deploy

## Operator

[Reference](https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/architecture.md)

    cd deploy/mongodb
    kubectl apply -f ./crd/mongodbcommunity.mongodb.com_mongodbcommunity.yaml
    kubectl create ns nuvolaris
    kubectl apply -k config/rbac/ --namespace nuvolaris

Verify resources

    kubectl get role mongodb-kubernetes-operator --namespace nuvolaris
    kubectl get rolebinding mongodb-kubernetes-operator --namespace nuvolaris
    kubectl get serviceaccount mongodb-kubernetes-operator --namespace nuvolaris

Install the operator

    kubectl create -f config/manager/manager.yaml --namespace nuvolaris

## Resources deployment

[Reference](https://github.com/mongodb/mongodb-kubernetes-operator/blob/master/docs/deploy-configure.md)

Just type your desired user password in the secret section of the file _mongodb.com_v1_mongodbcommunity_cr.yaml_, then run

    kubectl apply -f ./mongodb.com_v1_mongodbcommunity_cr.yaml --namespace nuvolaris

Verifiy resources creation

    kubectl get mongodbcommunity --namespace nuvolaris
    kubectl get po -n nuvolaris

Retrieve connection string from secret

    kubectl get secret example-mongodb-admin-my-user -n nuvolaris -o json | jq -r '.data | with_entries(.value |= @base64d)'

Check connection to the server with mongosh

    kubectl run -i --tty mongosh --image=rtsp/mongosh -n nuvolaris -- bash

When the mongosh container prompt comes up connect to the server using the connection string from the previous step, eg:

    mongosh "mongodb+srv://my-user:ow-str0ng-p4ssw0rd@example-mongodb-svc.nuvolaris.svc.cluster.local/admin?ssl=false"

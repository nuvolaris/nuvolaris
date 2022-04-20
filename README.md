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
# nuvolaris-operator

This is the Kubernetes Operator of the [bit.ly/nuvolaris](nuvolaris project). Follow the link to learn more.

You can discuss it in the #[nuvolaris-operator](https://discord.gg/RzJ4FHR2aR) discord channel and in the forum under the category [operator](https://github.com/nuvolaris/nuvolaris/discussions/categories/operator).

If you are interested in developing it, please read the [design document](DESIGN.doc). Please also read the [development environment document](https://github.com/nuvolaris/nuvolaris/blob/main/docs/DEVEL.md) to learn how to setup it.

## Developer notes

The operator is built in Python with [kopf](https://kopf.readthedocs.io/en/stable/). You can find some [examples here](https://github.com/nolar/kopf/tree/main/examples).

The operator uses under the hood [kustomize](https://kustomize.io/) and [kubectl](https://kubernetes.io/docs/reference/kubectl/) to interact with Kubernetes.

## Developing the operator

You can develop the operator without having to deploy it. Start it with `task dev:run`.  Then open another terminal and Use `task dev:apply` to apply the `deploy/nuvolaris-operator/whisk-dev.yml` file and `task dev:delete` to remove it. 

You can also interact with a python interpreter with the same libraries and some useful imports and configuration ready (most notably the autoreload) with `task dev:cli`. Check `TaskfileDev.yml` for other useful targets for cleanup and debug.

Finally, you can run unit tests with `task unit`, integration tests with `task integ`, both with `task test`, and select tests passing the variable  `T=<test-prefix>` on the task command line.
## Kubernetes Clusters

In order to test the operator against different clusters,  there are task scripts to also manage some clusters. Currently the following clusters  are: 

- `kind` 
- Amazon `eks` 
- Linode `lks` 

You can switch using one of the using some commands, with prefix the cluster name. Available commands are:

- `xxx:list`: list existing clusters
- `xxx:create`: create a test cluster
- `xxx:destroy`: destroy a test cluster
- `xxx:config`: set the kubeconfig to the current cluster

Note that kind is available in the development environment by defaut. You may want to use `task kind:config` to switch back to the current local cluster.

## Releasing the operator

Once the operator is ready, you can build and test it a against a kubernetes cluster.

First, generate a new image tag with `task image-tag`.

You can test locally using the kind cluster (provided by default by the development environment) with  `build-and-load`. 

To test it against other clusters, you need to build a public image on github. You can do it again generating an image tag and then pushing it to a publc repository. 

If you have push access to Nuvolaris repository just the tag to trigger the GitHub Action to buld and publish it. 

If you have your own reposityr, you can run

`task IMAGE=<userr>/nuvolaris-operator buildx-and-push`
 ## Testing the operator

First, [switch to the cluster](#kubernetes-cluster) you want to test with and [release the operator](#releasing-the-operator) accordingly.

Once you have the right cluster and the image properly published, you can test the operator with the following targets:

- `test:build-and-load`: build and load the operator in the cluster
- `test:deploy-operator`: deploys the operator in the current cluster.
- `test:deploy-instance`: deploy an instance of the configuration to build an actual cluster.
- `test:config-wsk`: once it is deployed, extracts the current configuration to use `wsk`
- `test:test-wsk`: runs a simple hello world test
- `test:destroy`: destroy the current deployment

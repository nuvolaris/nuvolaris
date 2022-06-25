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
# Nuvolaris Operator 

This is the Kubernetes Operator of the [bit.ly/nuvolaris](nuvolaris project).

You can discuss it in the #[nuvolaris-operator](https://discord.gg/RzJ4FHR2aR) discord channel and in the forum under the category [operator](https://github.com/nuvolaris/nuvolaris/discussions/categories/operator).

If you are interested in developing it, please read the [design document](DESIGN.doc). Please also read the [development environment document](https://github.com/nuvolaris/nuvolaris/blob/main/docs/DEVEL.md) to learn how to setup it.

## Developer notes

The operator is built in Python with [kopf](https://kopf.readthedocs.io/en/stable/). You can find some [examples here](https://github.com/nolar/kopf/tree/main/examples).

The operator uses under the hood [kustomize](https://kustomize.io/) and [kubectl](https://kubernetes.io/docs/reference/kubectl/) to interact with Kubernetes.

Let's discuss how to:

- Select the Kubernetes cluster to use
- Develop interactively (cli and tests)
- Run it without deploying
- Test it in a local cluster without pushing an image to a registry
- Push it to a public registry to use with external Kubernetes

## Selecting the Kubernetes Clusters

You have to run the operator against multiple clusters for test. So the operator has a provision to selection one to use and work with.

You can use other clusters for testing and development.  You should place all the configurations for the other clusters in the folder `clusters`, with extension `.kubeconfig`. See [below](#creating-a-new-cluster) for informations about this.

If you use the development environment, using Docker and VSCode, you have available a Kind cluster ready for test.  Use the task `task kind:config` to copy the configuration in the `clusters` folder if you plan to change cluster.

In order to test the operator against different clusters, you can list all the cluster configurations available with `task` and then select one with `task N` where N is the number of the configuration in the list shown.

Example:

```
$ task
*** current: kind
1 clusters/aks.kubeconfig
2 clusters/eks.kubeconfig
3 clusters/kind.kubeconfig
4 clusters/microk8s.kubeconfig
*** select with 'task #'
$ task 2
task: [2] task use N=2
cluster: eks
Kubeconfig user entry is using deprecated API version client.authentication.k8s.io/v1alpha1. Run 'aws eks update-kubeconfig' to update.
NAME                                              STATUS   ROLES    AGE   VERSION
ip-192-168-42-140.eu-central-1.compute.internal   Ready    <none>   49d   v1.22.6-eks-7d68063
```

## Developing the operator interactively

Start coding with `task cli`.

You can then develop some code experimentally interacting with a python interpreter with  the same libraries and some useful imports and configuration ready (most notably the autoreload).

You can then execute some tests.

- `task utest`: unit tests 
- `task itest`: integration tests

This will run all the tests. You can select which test to run with `tast itest T=xxx` or `task utest T=xxx`. It will then execute all the tests whose file starts with `xxx`.

## Developing the operator without deploying it

You can then start the whole operator without having to deploy it. Start it with `task run`.

Once you started the operarto pen another terminal and Use `task instance` to apply a crd instance depending on the current clusters.

The crd instance used it is defined by the type of kubernetes custer you are using. The script './detect.sh' tries to detect it. The configuration used is under `tests/<detected>/whisk.yaml`

If you have not changed the cluster the default cluster is 'kind' so it will apply the configuration `tests/kind/whisk.yaml`

You can change the configuration passing the `WHISK` parameter (without the .yaml).  So if you are running an `eks` cluster and you want to use your configuration `custom` the command `task instance WHISK=custom` will use `tests/eks/custom.yaml`

Other useful tasks:

- `task watch` starts watching deployed pods servics and nodes - useful to see what happens when you deploy 
- `task destroy` removes the instance but not the operator so you can recreate the cluster with `task instance` maybe with different parameters
- `task clean` removes everything including the operator and pvc
- If something get stuck and the cleanup does not complete `task defin` can help removing incomplete finalizers (you need to open another terminal to run it)

## Testing the operator deploying it locally

First and before all, you need a tag.

Execute `task image-tag`. This command will delete all the other tag and generate a tag in the format `x.y.z-milestone.timestamp`. This tag is essential to identify your operator.

When you are confident you can try the operator, in kind, use `task build-and-load`. This will build an instance and load it in the local kind. This step does not require you publish it to a public registry.

You can then proceed deploying it with `task operator` to deploy it.

You can then use `task instance` to deploy a crd instance, and finally `task actions` to test whisk running a few actions

## Publishing the operator

Once the operator is ready, you can build and test it a against a kubernetes cluster.

First, generate a new image tag with `task image-tag`.

You can test locally using the kind cluster (provided by default by the development environment) with  `build-and-load`. 

To test it against other clusters, you need to publish it to a public repository. 

If you have push access to Nuvolaris repository just push the tag and it will trigger the build using the tag to tag the repository and it will be published in the nuvolaris package registry on GitHub.

You can also publish an image to your own github repository for testing purposes. To do this, add to your `.env` the following variables:


```
MY_CONTROLLER_IMAGE=<your-user>/<your-name>
GITHUB_USER=<your-user>
GITHUB_TOKEN=<your-access-token>
```

You cannot override the tag of the operator you have to generate a git tag: `task image-tag`. Note the tag is unique for the current hour (it embeds: YYMMDDhh)

If you set those variables you can use 
- `task docker-login` to log to  
- `task build-and-push` to build for one single architecture (faster but limited to your architectur)
- `task buildx-and-push` to build for all the architectues (slower)

Remember that for GitHub Containter Registry you have to make public the image you are using to tlet it to be accessible by other Kubernetes

### Running tests

Once you have choosen the Kubernetes cluster and published the images on a public registry you can test it with  `task dtest`, that will run a complete deployment in the current Kubernetes cluster.

If you want to run all the tests (u, i, d) aginst the current cluster use `task test`

Finally if you want to run the tests against all the configured kubernetes use `task all-kubes -- <target>`.

This targes runs a group of tests against all the available clusters, so you can run all the tests against all the kubes with `task all-kubes -- test`

# Reference

- `use` (default task) lists all the clusters; 
- `1`, `2`...`9` selects the corresponding entry
- `operator`: deploys the operator in the current cluster.
- `instance`: deploy an instance of the configuration to build an actual cluster.
- `destroy`: destroy the current deployment
- `clean`: remove everything - if you get stuck use `defin`
- `defin`:  remove finalizer for the controller, useful if `clean` does not complete
- `config`: once it is deployed, extracts the current configuration to use `wsk`
- `actions`: deploy and run test actions
- `utest` runs unit tests, filter with `T=<xxx>`
- `itest` runs integration tests, filter with `T=<xxx>`
- `dtest` deployment test
- `hello`: runs a simple hello world test
- `ping`: runs a ping test of redis
- `all-kubes -- <target>`: execute the `<target>` against all the configured kubes

Build targets

- `b:buildx-and-push`: build and push the operator in multiple architectectures (slow)
- `b:build-and-load`: build and load the operator in the kind cluster
- `b:docker-login`: login into the github docker registry 
- `b:build-and-push`: build and push the operator in the current architecture

Currently the following clusters are supported: 

- Kubernetes `kind` 
- Amazon `eks`
- Azure `aks`
- Google `gke`
- Ubuntu `microk8s`

See below for creating clusters and configurations. All the configuration for the available clusters are expected to be in `clusters/*.kubeconfig`

Available commands for the cluster `xxx` (not always and not for all the cases):

- `xxx:list`: list existing clusters
- `xxx:create`: create a test cluster
- `xxx:destroy`: destroy a test cluster
- `xxx:config`: set the kubeconfig to the current cluster

Note that `kind` is available in the development environment by defaut. You may want to use `task kind:config` to extract the configuration to be able to switch back to the local clusters.


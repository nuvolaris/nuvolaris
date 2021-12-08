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
# Nuvolaris Roadmap

Version 0.1, November 2021. Subject to changes.

 ## About

Nuvolaris will be a distribution of Apache OpenWhisk. It will be open source and released under the Apache License.

It should let you to install itself on any supported Kubernetes with a single command:

```
curl get.nuvolaris.org | kubectl apply -f -
```

This will give sensible defaults. We can then use [`kustomize`](https://kustomize.io/) to further customize options. Ideally the whole configuration should be a single file as simple as possible.

This command will basically install an operator that will perform all the operations to setup OpenWhisk and his dependencies and additions.

The core of our work will be to build such an operator.

We will use the OpenWhisk code base as much as possible and contribute back our changes, but we will buld it as an independent and integrated product, more or less as the other project partecipants are building their own cloud offering. 

## Targets

It should run and be tested to work on more recent versions of:

- Amazon EKS
- Azure AKS
- Google GKE
- Redhat OpenShift 
- Rancher K3S
- Ubuntu MicroK8s 

More Kubernetes distributions we can add the better.

It should be able to autodetect the environments where is going to run.
  
## Operators

All the components must be managed with Operators.

It should be installable in a scalable way. It should be installable without any component, then adding optionally CouhchDB and Kafka.

It should be possible to enable alternatives, for example using Mongodb instead of Couchdb, or Redpanda instead of Kafka.

And it should be possible to use either locally installed or cloud versions of those operators.

## Additional Components

The installer shold be able to use or connect to those external compoments:

- a cache based on redis
- object storage compatible s3
- a SQL database service, either MySQL or Postgresql
- a NO-SQL database service, either Couchdb or Mongodb
- a DynamoDB compatible database service, for example Scylla Alternator

## Runtimes

- stardardize all the runtimes on ActionLoop 
- build all of them from a single repository
- publish all the runtimes on GitHub 
- use a consistent set of libraries to access easily the supported components
- provides a standardized way to initialize the support component (ideally automatically from environment variables)
- use only standard libraries, avoiding customized and proprietary runtimes. 

Ideally, Nuvolaris applications should work in every OpenWhisk implementations (IBM, Adobe, Naver, DigitalOcean) as long as a configuration file to connect to additional services is provided.
    
## Lambda Compatibility

- It should be possible to run Lambda Actions with a compatibilty layer
- It should be possible to support actions using DynamodDB through a compatible database

## Development Tools

We have to provide together with the runtimes, the required build to reconstruct a local environent to run tests and develop without having to deploy the project.

## Legacy Migrations

We need to provide support tools allowing to migrate SpringBoot as serverless applications with minimal (ideally zero) code changes.

We need to support Wordpress to be usable as a  provider of content for JAMStack applications, ideally building it as a serverless action.

## Integrations

We need to integrate Kafka as a serverless provider

We need to integrate Spark as a serverless provider

We need to integrate Tensorflow as a serverless provider.
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

Version 0.2, February 2022. Subject to changes.

## About

Nuvolaris will be a distribution of Apache OpenWhisk. It will be open source and released under the Apache License.

The entire platform will be managed by a single CLI allowing both to administer the platform and develop with it.

The platform itself is managed by ab operator, that installs OpenWhisk, and its dependencies and additions.

The core of our work will be to build such an operator.

We will use the OpenWhisk code base as much as possible and contribute back our changes, but we will buld it as an independent and integrated product, more or less as the other project partecipants are building their own cloud offering.

## Targets

It should run and be tested to work on more recent versions of:

- Amazon EKS
- Azure AKS
- Google GKE
- Redhat OpenShift
- Ubuntu Charmed Kubernetes
- Rancher K3S
- VMware Tanzu

More Kubernetes distributions we can add the better.

It should be able to autodetect the environments where is going to run.

## Operators

All the components must be managed with Operators.

It should be installable in a scalable way. It should be installable without any component, then adding optionally CouchDB and Kafka.

It should be possible to enable alternatives, for example using Mongodb instead of Couchdb, or Redpanda instead of Kafka.

And it should be possible to use either locally installed or cloud versions of those operators.

## Additional Components

The installer should be able to use or connect to those external compoments:

- a object storage compatible with s3
- a cache based on redis
- a SQL database service, either MySQL or PostgreSQL
- a NO-SQL database service, either Couchdb or Mongodb

## Runtimes

- stardardize all the runtimes on ActionLoop
- build all of them from a single repository
- publish all the runtimes on GitHub
- use a consistent set of libraries to easily access the supported components
- provides a standardized way to initialize the support component (ideally automatically from environment variables)
- use only standard libraries, avoiding customized and proprietary runtimes.

Ideally, Nuvolaris applications should work in every OpenWhisk implementation (IBM, Adobe, Naver, DigitalOcean) as long as a configuration file to connect to additional services is provided.

## Development Tools

We have to provide, together with the runtimes, the required build to reconstruct a local environent to run tests and develop without having to deploy the project.

## Legacy Migrations

We need to provide support tools allowing to migrate SpringBoot as serverless applications with minimal (ideally zero) code changes.

We need to support Wordpress to be usable as a provider of content for JAMStack applications, ideally building it as a serverless action.

## Integrations

We will integrate enterprise products like
- Kafka for streaming applications
- Spark for big data applications
- TensowrFlow for deep learning applications

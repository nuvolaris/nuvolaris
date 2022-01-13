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
FROM ubuntu:20.04
ENV STANDALONE_IMAGE=ghcr.io/nuvolaris/openwhisk-standalone
ENV STANDALONE_TAG=neo-21.1230.16
# configure dpkg && timezone
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# add docker and java (amazon corretto) repos
RUN apt-get update && apt-get -y upgrade && apt-get -y install python3.9 python3.9-venv curl sudo
RUN useradd -m -s /bin/bash nuvolaris &&\
    echo "nuvolaris ALL=(ALL:ALL) NOPASSWD: ALL" >>/etc/sudoers
USER nuvolaris
WORKDIR /home/nuvolaris
RUN curl -sSL https://install.python-poetry.org | python3.9 -
ADD pyproject.toml poetry.lock /home/nuvolaris/
ADD nuvolaris/*.py /home/nuvolaris/nuvolaris/
ADD deploy /home/nuvolaris/deploy/
ENV PATH=/home/nuvolaris/.local/bin:/usr/local/bin:/usr/bin:/sbin:/bin
RUN poetry install
CMD poetry run kopf run -n nuvolaris -m nuvolaris nuvolaris/main.py

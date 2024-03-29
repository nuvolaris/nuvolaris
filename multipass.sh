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
if ! which multipass
then echo "Please install multipass"; exit 1
fi

if test "$1" == "reset"
then 
   multipass delete nuvolaris
   multipass purge
fi

if ! multipass ls | grep nuvolaris
then 
   echo Preparing nuvolaris vm - expect a timeout
   multipass launch -c4 -m8G -d50G -nnuvolaris --cloud-init cloud-init.yaml
fi

multipass shell nuvolaris

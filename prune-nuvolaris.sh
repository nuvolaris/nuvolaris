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
#!/bin/bash
############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Utility to remove containers started by Nuvolaris development environment."
   echo
   echo "Syntax: prune-nuvolaris [-q|h]"
   echo "options:"
   echo "q     Quiet mode (skip user confirmation)."
   echo "h     Print this Help."
   echo
}
PruneNuvolaris()
{
  cnt=$(docker ps -f name=nuvolaris -aq | wc -l)
  if [ $cnt -gt 0 ]
  then 
    docker ps -f name=nuvolaris -aq | xargs docker kill
    docker ps -a | grep vsc-nuvolaris | cut -d' ' -f1 | xargs docker kill
  else
    echo "No Nuvolaris worker/controller running."
  fi
  cnt=$(docker ps -f name=nuvolaris -aq | wc -l)
  if [ $cnt -gt 0 ]
  then 
    docker ps -f name=nuvolaris -aq | xargs docker rm
    docker ps -a | grep vsc-nuvolaris | cut -d' ' -f1 | xargs docker rm
  else
    echo "No Nuvolaris VS Code devcontainer running."
  fi
}

quiet=false
while getopts ":h:q" option; do
  case $option in
    h) # display Help
      Help
      exit;;
    q) # quiet mode
      quiet=true;;
    \?) # Invalid option
      echo "Error: Invalid option"
      Help
      exit;;
  esac
done

if [ "$quiet" = true ] 
then
  PruneNuvolaris
else
  echo "Use -q option to skip confirmation."
  echo -n "Do you want to stop and remove all Nuvolaris related containers (Y/N)? "
  read confirm
  if [ "$confirm" = "Y" ] 
  then
    PruneNuvolaris
  fi
fi

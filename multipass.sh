#!/bin/bash
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
   multipass launch -c4 -m4G -d30G -nnuvolaris --cloud-init cloud-init.yaml
fi

multipass shell nuvolaris

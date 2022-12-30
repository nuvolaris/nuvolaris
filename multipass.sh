if [[ "$1" = "reset" ]]
then multipass delete devkit
     multipass purge
fi
multipass launch -c2 -m4G -d30G --cloud-init cloud-init.yaml -n devkit
echo it can timeout because the setup can take more time

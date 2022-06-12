# Expose MicroK8s Apihost externally

If you want to access to the server remotely, you need to add the DNS name of the server (either the real one or the .nip.io) and  generate a proper configuration with:

```
DNS='<your-dns-name>'
sudo microk8s stop
sed -i "/DNS.5/a DNS.6 = $DNS" /var/snap/microk8s/current/certs/csr.conf.template
sudo microk8s start
microk8s config | sed -e "s/server: .*/server: https:\/\/$DNS:16443/" >kubeconfig
```

You can then download the kubeconfig file and copy in your ~/.kube/config to access the remote Kubernetes cluster.

Then you can then [donwload `nuv`](https://github.com/nuvolaris/nuvolaris/releases) and [install](SETUP.md#kubernetes-installation) Nuvolaris from the server itself with `nuv setup --context=<context>`.



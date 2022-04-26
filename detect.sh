#!/bin/bash
LABELS="$(kubectl get nodes -ojsonpath='{.items[].metadata.labels}' 2>/dev/null)"
if echo "$LABELS" | jq . | grep eksctl.io >/dev/null
then echo "eks"
elif echo "$LABELS" | jq . | grep microk8s.io >/dev/null
then echo "microk8s"
elif echo "$LABELS" | jq . | grep lke.linode.com >/dev/null
then echo "lks"
elif echo "$LABELS" | jq . | awk '/nuvolaris.io\/kube/ {print $2}' | grep kind >/dev/null
then echo "kind"
else echo "generic"
fi
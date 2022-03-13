import nuvolaris.kustomize as nku
import nuvolaris.kube as kube
import os, os.path
import logging

WHISK_IMG = os.environ.get("STANDALONE_IMAGE", "ghcr.io/nuvolaris/openwhisk-standalone")
WHISK_TAG = os.environ.get("STANDALONE_TAG", "latest")

def whisk_create():
    spec = nku.kustom_list("openwhisk-standalone", nku.image(WHISK_IMG, newTag=WHISK_TAG))
    #kopf.adopt(spec)
    #logging.debug(spec)
    return kube.apply(spec)


def whisk_delete():
    spec = nku.kustom_list("openwhisk-standalone", nku.image(WHISK_IMG, newTag=WHISK_TAG))
    return kube.apply(spec)

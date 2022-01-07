import kopf
import os.path
import nuvolaris.kustomize as nku

@kopf.on.login()
def whisk_login(**kwargs):
    token = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    if os.path.isfile(token):
        return kopf.login_via_pykube(**kwargs)
    return kopf.login_via_client(**kwargs)

@kopf.on.create('whisks')
def whisk_create(spec, **kwargs):
    # TODO: pass from configurations somewhere
    print("whisk_create")
    TAG = "neo-21.1230.16"
    IMG = "ghcr.io/nuvolaris/openwhisk-standalone"
    yaml = nku.kustomize("openwhisk-standalone", nku.image(IMG, newTag=TAG))
    print(yaml)
    return {'message': 'created'}


@kopf.on.delete('whisks')
def whisk_delete(spec, **kwargs):
    print("whisk_delete")
    return {'message': 'deleted'}


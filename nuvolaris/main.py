import kopf
import os.path

@kopf.on.login()
def whisk_login(**kwargs):
    token = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    if os.path.isfile(token):
        return kopf.login_via_pykube(**kwargs)
    return kopf.login_via_client(**kwargs)



@kopf.on.create('whisks')
def whisk_create(spec, **kwargs):
    print(f"Creating: {spec}")
    return {'message': 'created'}


@kopf.on.delete('whisks')
def whisk_delete(spec, **kwargs):
    print(f"Deleting: {spec}")
    return {'message': 'deleted'}



import flatdict, json

_config = None
_name = None

# define a configuration singleton with a name
# update to the configurations should retain that name
# delete the configuration
def configure(name: str, spec: dict, labels: list = []):
    global _config, _name
    if _config:
        if name != _name:
            return False
    _name = name
    _config = dict(flatdict.FlatDict(spec, delimiter="."))

    for i in labels:
        for j in list(i.keys()):
            if j.startswith("nuvolaris-"):
                _config[ j[10:] ] = i[j]

    return True

def get(key):
    if _config:
        return _config.get(key)
    return None

def getall(prefix):
    res = []
    if _config:
        for key in _config.keys():
            if key.startswith(prefix):
                res.append(_config[key])
    return res

def keys(prefix=""):
    res = []
    if _config:
        for key in _config.keys():
            if key.startswith(prefix):
                res.append(key)
    return res

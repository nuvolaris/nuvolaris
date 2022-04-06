from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import create_autospec

kfn = create_autospec(kube.kubectl, return_value="ok")
p = patch('nuvolaris.kube.kubectl', kfn)
p.start()
openwhisk.create()
kube.kubectl("boh")
p.stop()
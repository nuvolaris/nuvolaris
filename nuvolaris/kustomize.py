# this module wraps generation of kustomizations

import os
import nuvolaris.kube as kube

# execute the kustomization of a folder under "deploy"
# sperficied with `where`
# it generate a kustomization.yaml, adding the header 
# then including all the files of that folder as resources
# you have to pass a list of kustomizations to apply
# you can use various helpers in this module to generate customizations
# it returns the expanded kustomization
def kustomize(where, *what):
    """Test kustomize

    >>> import nuvolaris.kustomize as ku
    >>> import nuvolaris.testutil as tu
    >>> tu.grep(ku.kustomize("test", ku.image("busybox", "nginx")), "kind|image:")
    kind: Pod
    - image: nginx
    """
    # prepare the kustomization
    dir = f"deploy/{where}"
    tgt = f"{dir}/kustomization.yaml"
    with open(tgt, "w") as f:
        f.write("apiVersion: kustomize.config.k8s.io/v1beta1\nkind: Kustomization\n")
        for s in list(what):
            f.write(s)
        f.write("resources:\n")
        for file in os.listdir(f"deploy/{where}"):
            if file != "kustomization.yaml":
                f.write(f"- {file}\n")
    return kube.kubectl("kustomize", dir)


# generate image kustomization
def image(name, newName=None, newTag=None):
    """Test image

    >>> import nuvolaris.kustomize as ku
    >>> print(ku.image("busybox"), end='')
    images:
    - name: busybox
    >>> print(ku.image("busybox", "nginx"), end='')
    images:
    - name: busybox
      newName: nginx
    >>> print(ku.image("busybox", newTag="nightly"), end='')
    images:
    - name: busybox
      newTag: nightly
    >>> print(ku.image("busybox", "nginx", "nightly"), end='')
    images:
    - name: busybox
      newName: nginx
      newTag: nightly
    """
    r = f"images:\n- name: {name}\n"
    if newName: r += f"  newName: {newName}\n"
    if newTag:  r += f"  newTag: {newTag}\n"
    return r





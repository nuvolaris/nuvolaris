import nuvolaris.kube as kube

def common():
    """
    >>> from nuvolaris import kustom 
    >>> import testutil
    >>> kustom.mode = "kustomize"
    >>> kustom.common()
    >>> testutil.grep(kustom.output, r"^kind:")
    kind: Namespace
    kind: ServiceAccount
    kind: Role
    kind: RoleBinding
    >>> kustom.mode = "apply"
    >>> kustom.common()
    True
    >>> _ = os.system("kubectl -n nuvolaris get serviceaccount standalone -o jsonpath='{.metadata.name}'") ; print()
    standalone
    >>> kustom.mode = "delete"
    >>> kustom.common()
    True
    """
    return kube.kustomize("common", "")


def standalone(tag):
    """
    >>> import nuvolaris.kustom as kustom
    >>> import testutil
    >>> kustom.mode = "kustomize"
    >>> kustom.standalone("neo-22.0304.05")
    True
    >>> testutil.grep(kustom.output, "image:")
    - image: ghcr.io/nuvolaris/openwhisk-standalone:neo-22.0304.05
    """
    return kube.kustomize("openwhisk-standalone", f"""
images:
- name: ghcr.io/nuvolaris/openwhisk-standalone
  newTag: {tag}
""")
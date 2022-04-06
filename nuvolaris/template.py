
import os

from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader(["./nuvolaris/templates", "./nuvolaris/files"])
env = Environment(loader=loader)

# expand template
def expand_template(template, data):
    """
    >>> import json
    >>> json.loads(expand_template("test.json", {"item": "hello"}))
    {'_id': 'test', 'value': 'hello'}
    """
    tpl = env.get_template(template)
    return tpl.render(data)
    #doc = json.loads(tpl.render(data))


# expond template and save in a file
def spool_template(template, file, data):
    """
    >>> import nuvolaris.testutil as tu
    >>> tu.grep(tu.fread(spool_template("test.json", "/tmp/test.json", {"item": "hi"})), r"value")
    "value": "hi"
    """
    with open(file, "w") as f:
        f.write(expand_template(template, data))
    return file

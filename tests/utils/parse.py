from jsonpickle import json


def toJSon(object):
    return json.loads(json.dumps(object._attributes))

import json
import os


def call_read_return(imp, func, src):
    print("Calling function {0}".format(func))
    f = getattr(imp, func)
    f(src, "{0}.json".format(func))
    with open("{0}.json".format(func), "r", encoding='utf-8') as file:
        obj = json.load(file)
        obj['id'] = func
    os.remove("{0}.json".format(func))
    print("Got result from {0}".format(func))
    return obj

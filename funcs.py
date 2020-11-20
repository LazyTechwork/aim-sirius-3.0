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


def call_read_return_multiple(imp, func, src, variants):
    print("Calling function {0}".format(func))
    f = getattr(imp, func)
    f(src, "{0}_".format(func))
    obj = list()
    for variant in variants:
        with open("{0}_{1}.json".format(func, variant), "r", encoding='utf-8') as file:
            js_obj = json.load(file)
            js_obj['id'] = func
            obj.append(js_obj)
        os.remove("{0}_{1}.json".format(func, variant))
        print("Got result from {0} / {1}".format(func, variant))
    return obj

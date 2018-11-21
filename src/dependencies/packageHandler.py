import requests
import json
import os
from pprint import pprint
import sys

DEPENDENCIES_PACKAGE_KEY = 'dependencies'
DEV_DEPENDENCIES_PACKAGE_KEY = 'devDependencies'


def process(inputfile, url, repository_id):
    if url is '':
        raise ValueError('url should not be empty')
    if repository_id is '':
        raise ValueError('repository_id should not be empty')

    dependencies = getDependancies(inputfile)
    dependencies = builtDependanciesModules(dependencies)
    api_url = url.rstrip('/') + '/' + repository_id

    r = postJson(api_url, dependencies)
    if r.status_code not in (200, 201):
        pprint(r.request)
        pprint(r.status_code)
        pprint(r.url)
        pprint(r.content)
        sys.exit(1)
    print 'POST ' + str(len(dependencies)) + ' Modules to : ' + api_url
    sys.exit()


def getDependancies(inputfile):
    if os.path.exists(inputfile):
        with open(inputfile) as f:
            data = json.load(f)
            dependencies = mergeDicts(data.get(DEPENDENCIES_PACKAGE_KEY), data.get(DEV_DEPENDENCIES_PACKAGE_KEY))
            return dependencies
    else:
        raise ValueError(inputfile + ' : File not exists')


def mergeDicts(x, y):
    if isinstance(x, dict) and len(x) and isinstance(y, dict) and len(y):
        z = x.copy()
        z.update(y)
        return z
    elif isinstance(x, dict) and len(x) and (not isinstance(y, dict) or not len(y)):
        return x
    elif isinstance(y, dict) and len(y) and (not isinstance(x, dict) or not len(x)):
        return y
    else:
        return {}


def builtDependanciesModules(dependencies):
    ret = []
    for dependency in dependencies.items():
        ret.append(moduleItem(dependency))
    return ret


def moduleItem(dependency):
    return {
        'spec': dependency[0],
        'version': dependency[1]
    }


def postJson(url, payload, headers={}):
    return requests.post(url, headers=headers, json=payload, verify=False)

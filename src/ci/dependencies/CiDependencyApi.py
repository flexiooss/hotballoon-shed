import requests
import json
import os
from pprint import pprint
import sys


class CiDependencyApiUrl:
    REPOSITORIES = 'repositories'
    PRODUCES = 'produces'
    DEPENDS_ON = 'depends-on'

    base_url = ''  # type: str
    repository_id = ''  # type: str

    def __init__(self, base_url, repository_id):
        self.base_url = base_url.rstrip('/') + '/'
        self.repository_id = repository_id

    def repository(self):
        return self.base_url + self.REPOSITORIES + '/' + self.repository_id

    def produces(self):
        # type: () -> str
        return self.repository + '/' + self.PRODUCES

    def depends_on(self):
        # type: () -> str
        return self.repository + '/' + self.DEPENDS_ON


class CiDependencyApiHandler:
    ci_dependency_api_url = None  # type: CiDependencyApiUrl
    VERIFY_SSL = False  # type: bool
    repository = ''  # type: str
    checkout_spec = ''  # type: str

    def __init__(self, repository, checkout_spec, ci_dependency_api_url):
        # type: (str, str, CiDependencyApiUrl)-> None

        self.repository = repository
        self.checkout_spec = checkout_spec
        if not isinstance(ci_dependency_api_url, CiDependencyApiUrl):
            raise TypeError('ci_dependency_api_url should be an instance of CiDependencyApiUrl')
        self.ci_dependency_api_url = ci_dependency_api_url

    def put_repo_meta(self):
        # type: () -> requests.Response
        print "uploading repo metas : "

        repo = {
            'name': self.repository,
            'checkoutSpec': self.checkout_spec
        }
        pprint(repo)

        return requests.put(
            self.ci_dependency_api_url.repository,
            json=repo,
            verify=self.VERIFY_SSL
        )

    def post_produced(self, produces):
        # type: (list) -> requests.Response
        print "uploading produced modules meta : "
        pprint(produces)

        return requests.post(
            self.ci_dependency_api_url.produces(),
            json=produces,
            verify=self.VERIFY_SSL
        )

    def post_depends_on(self, dependencies):
        # type: (list) -> requests.Response
        print "uploading depends-on modules meta :"
        pprint(dependencies)

        return requests.post(
            self.ci_dependency_api_url.depends_on(),
            json=dependencies,
            verify=self.VERIFY_SSL
        )

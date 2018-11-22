#!/usr/bin/python

import re
import os
import sys
import getopt
from pprint import pprint
from PackageHandler import PackageHandler
from CiDependencyApi import CiDependencyApiUrl, CiDependencyApiHandler
from ProducesHandler import ProducesHandler


def main(argv):
    repository, repository_id, checkout_spec = get_env()
    package_file, dependencies_url, docker_image = parse_options(argv)

    api_handler = CiDependencyApiHandler(
        repository=repository,
        checkout_spec=checkout_spec,
        ci_dependency_api_url=CiDependencyApiUrl(
            base_url=dependencies_url,
            repository_id=repository_id
        )
    )

    package_handler = PackageHandler(
        package_file=package_file,
        repository=repository
    ).process()

    produces_handler = ProducesHandler(
        docker_image=docker_image,
        repository=repository,
        version=package_handler.version
    ).process()

    r = api_handler.put_repo_meta()
    if r.status_code not in 200:
        log_response(r)
        sys.exit(1)

    r = api_handler.post_produced(produces=produces_handler.produces)
    if r.status_code not in 201:
        log_response(r)
        sys.exit(1)

    r = api_handler.post_depends_on(dependencies=package_handler.dependencies)
    if r.status_code not in 201:
        log_response(r)
        sys.exit(1)
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])


def get_env():
    repository = os.environ['REPOSITORY']
    repository_id = os.environ['REPOSITORY_ID']
    checkout_spec = os.environ['CHECKOUT_SPEC']

    return repository, repository_id, checkout_spec


def parse_options(argv):
    package_file = ''  # type: str
    dependencies_url = ''  # type: str
    docker_image = ''  # type: str

    try:
        opts, args = getopt.getopt(argv, "hi:u:d", ["help", "ifile=", "url=", "docker_image="])
    except getopt.GetoptError:
        print 'hotballoon-shed:ci:dependencies:meta -i <package_file> -u <dependencies_url> -d <docker_image>'
        sys.exit(2)

    for opt, arg in opts:
        arg = re.sub('[\s+]', '', arg)
        if opt in ("-h", "--help"):
            print 'hotballoon-shed:ci:dependencies:meta -i <package_file> -u <dependencies_url> -d <docker_image>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            package_file = arg
        elif opt in ("-u", "--url"):
            dependencies_url = arg
        elif opt in ("-d", "--docker_image"):
            docker_image = arg

    return package_file, dependencies_url, docker_image


def log_response(response):
    pprint(response.request)
    pprint(response.status_code)
    pprint(response.url)
    pprint(response.content)

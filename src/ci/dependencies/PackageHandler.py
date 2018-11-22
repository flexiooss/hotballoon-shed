import json
import os
import re
from ModuleHandler import ModuleHandler


class PackageHandler(ModuleHandler):
    DEPENDENCIES_PACKAGE_KEY = 'dependencies'
    DEV_DEPENDENCIES_PACKAGE_KEY = 'devDependencies'
    VERSION_KEY = 'version'

    dependencies = []  # type: list
    version = ''  # type: str

    def __init__(self, package_file, repository):
        # type: (str, str) -> None
        if not os.path.exists(package_file):
            raise ValueError(package_file + ' : File not exists')

        self.package_file = package_file
        self.repository = repository

    def process(self):
        self.dependencies = self._built_dependencies_modules(
            self._get_package_dependencies()
        )
        return self

    def _get_package_dependencies(self):
        # type: () -> dict
        with open(self.package_file) as f:
            data = json.load(f)
            dependencies = self.merge_dicts(
                data.get(self.DEPENDENCIES_PACKAGE_KEY),
                data.get(self.DEV_DEPENDENCIES_PACKAGE_KEY)
            )
            self.version = data.get(self.VERSION_KEY, '')
            return dependencies

    def _built_dependencies_modules(self, dependencies):
        # type: (dict) -> list

        ret = []
        for dependency in dependencies.items():
            ret.append(
                self.module_item(
                    self.SPEC_JS_PREFIX + dependency[0],
                    self._process_version(dependency[1])
                )
            )
        return ret

    def _process_version(self, package_version):
        # type: (str) -> str
        if package_version.find('.git') is -1:
            return re.sub(r'[^\d.]', '', package_version)
        else:
            detail = package_version.split('#')
            if len(detail) > 1:
                return '#'.join(detail[1:])
            else:
                return self.DEFAULT_VERSION

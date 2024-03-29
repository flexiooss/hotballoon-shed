from typing import List, Set, Dict

from cmd.package.PackageHandler import PackageHandler

from cmd.package.WalkerProcessor import WalkerProcessor
from cmd.package.Version import Version


class PeerDependenciesWalkerProcessor(WalkerProcessor):
    dependencies: Dict[str, str]

    def __init__(self) -> None:
        self.dependencies = {}

    def count(self) -> int:
        return len(self.dependencies)

    def process(self, package: PackageHandler):

        if self.dependencies.get(package.name()) is not None:

            if not Version(self.dependencies.get(package.name())).satisfies(package.version()):
                raise ImportError(
                    'Version conflict with package : ' + package.name() + ':' + package.version() + ' version : ' + self.dependencies.get(
                        package.name()) + ' already registered')
        else:
            self.dependencies[package.name()] = package.version()

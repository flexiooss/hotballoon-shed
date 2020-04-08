from typing import List, Set

from cmd.package.PackageHandler import PackageHandler

from cmd.package.WalkerProcessor import WalkerProcessor


class PeerDependenciesWalkerProcessor(WalkerProcessor):
    dependencies: Set[str]

    def __init__(self) -> None:
        self.dependencies = set([])

    def process(self, package: PackageHandler):
        self.dependencies.add(package.name())

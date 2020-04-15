from typing import List, Set, Dict, Optional

from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.PackageHandler import PackageHandler

from cmd.package.WalkerProcessor import WalkerProcessor


class ExternalModulesDependenciesProcessor:
    dependencies: Set[str]

    def __init__(self) -> None:
        self.dependencies = set([])

    def count(self) -> int:
        return len(self.dependencies)

    def add(self, dependency: str):
        self.dependencies.add(dependency)

    def add_all(self, package: PackageHandler):
        hb_package: Optional[HBShedPackageHandler] = HBShedPackageHandler.from_package_handler(package)

        if hb_package is not None:

            if hb_package.config().has_dependencies():
                dependendency: str
                for dependendency in hb_package.config().dependencies():
                    self.dependencies.add(dependendency)

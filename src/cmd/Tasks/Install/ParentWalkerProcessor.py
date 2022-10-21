from typing import List, Set, Dict, Optional

from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.PackageHandler import PackageHandler

from cmd.package.WalkerProcessor import WalkerProcessor


class ParentWalkerProcessor(WalkerProcessor):
    parents: Dict[str, str]

    def __init__(self) -> None:
        self.parents = {}

    def count(self) -> int:
        return len(self.parents)

    def __cleanVersion(self, version: str) -> bool:
        return re.sub('[~^<=>*]', '', version)

    def process(self, package: PackageHandler):
        hb_package: Optional[HBShedPackageHandler] = HBShedPackageHandler.from_package_handler(package)

        if hb_package is not None:

            if hb_package.config().has_parent_external():

                if self.parents.get(hb_package.config().parent_name()):

                    if hb_package.config().has_parent_version() \
                            and self.parents.get( hb_package.config().parent_name()) is not None \
                            and self.__cleanVersion(self.parents.get(hb_package.config().parent_name())) != self.__cleanVersion(hb_package.config().parent_version()):
                        raise ImportError(
                            'Version conflict with parent package : ' + package.name() + ' parent: ' + hb_package.config().parent_name() + ' version:' + hb_package.config().parent_version() + ' because version : ' + self.parents.get(
                                hb_package.config().parent_name()) + ' already registered')

                self.parents[hb_package.config().parent_name()] = hb_package.config().parent_version()

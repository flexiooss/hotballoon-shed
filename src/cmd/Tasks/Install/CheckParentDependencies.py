import sys
from pathlib import Path
from typing import Optional, List, Dict, Set
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.PackageHandler import PackageHandler


class CheckParentDependencies:

    def __init__(self, root_package: Optional[HBShedPackageHandler], dependencies: Set[str]) -> None:
        self.__root_package: Optional[HBShedPackageHandler] = root_package
        self.__node_modules: Path = root_package.modules_path()
        self.__dependencies: Set[str] = dependencies

    def __get_package(self, name: str) -> PackageHandler:
        target_path: Path = self.__node_modules.joinpath(name)
        if not target_path.is_dir():
            raise FileNotFoundError(
                'Package : ' + name + ' not found at : ' + self.__node_modules.as_posix())
        return PackageHandler(target_path)

    def process(self):
        for name in self.__dependencies:
            sys.stdout.write('*')
            sys.stdout.flush()
            package: PackageHandler = self.__get_package(name)

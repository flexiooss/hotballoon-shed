import sys
from pathlib import Path
from typing import Optional, List, Dict
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.PackageHandler import PackageHandler


class CheckParents:

    def __init__(self, root_package: Optional[HBShedPackageHandler], parents: Dict[str, Optional[str]]) -> None:
        self.__root_package: Optional[HBShedPackageHandler] = root_package
        self.__node_modules: Path = root_package.modules_path()
        self.__parents: Dict[str, Optional[str]] = parents

    def __get_package(self, name: str) -> PackageHandler:
        target_path: Path = self.__node_modules.joinpath(name)
        if not target_path.is_dir():
            raise FileNotFoundError(
                'Package : ' + name + ' not found at : ' + self.__node_modules.as_posix())
        return PackageHandler(target_path)

    def process(self):
        for name, version in self.__parents.items():
            sys.stdout.write('*')
            sys.stdout.flush()
            package: PackageHandler = self.__get_package(name)
            if version is not None and package.version() != version:
                sys.stderr.write("\n")
                sys.stderr.flush()
                raise ImportError('package: ' + name + ' is on version: ' + package.version() + ' parents required: ' + version)

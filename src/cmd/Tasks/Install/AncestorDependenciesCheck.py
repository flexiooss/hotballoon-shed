import sys
from pathlib import Path
from typing import Optional, List, Dict, Set
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.PackageHandler import PackageHandler


class AncestorDependenciesCheck:

    def __init__(self, root_package: HBShedPackageHandler, package: HBShedPackageHandler,
                 dependencies: Set[str]) -> None:
        self.__root_package: HBShedPackageHandler = root_package
        self.__package: HBShedPackageHandler = package
        self.__node_modules: Path = root_package.modules_path()
        self.__dependencies: Set[str] = dependencies

    def __get_package(self, name: str) -> Optional[HBShedPackageHandler]:
        target_path: Path = self.__node_modules.joinpath(name)
        if not target_path.is_dir():
            raise FileNotFoundError(
                'Package : ' + name + ' not found at : ' + self.__node_modules.as_posix())
        return HBShedPackageHandler.from_package_handler(PackageHandler(target_path))

    def process(self):
        if self.__package.has_dependencies():
            name: str
            for name in self.__dependencies.copy():
                if self.__package.dependencies().get(name) is not None:
                    sys.stdout.write('*')
                    sys.stdout.flush()
                    self.__dependencies.remove(name)

        if len(self.__dependencies) and self.__package.config().has_parent_external():
            parent: Optional[HBShedPackageHandler] = self.__get_package(self.__package.config().parent_name())
            if parent is not None:
                AncestorDependenciesCheck(
                    root_package=self.__root_package,
                    package=parent,
                    dependencies=self.__dependencies
                ).process()

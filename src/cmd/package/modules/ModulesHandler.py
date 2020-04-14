from pathlib import Path
from typing import List

from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.modules.Module import Module


class ModulesHandler:
    modules: List[Module]

    def __init__(self, package: HBShedPackageHandler) -> None:
        self.__package: HBShedPackageHandler = package
        self.modules: List[Module] = []
        self.__load_modules()

    def __check_parent_version(self, module: Module):
        if not module.package.config().has_parent() or module.package.config().parent_name() != self.__package.name():
            raise AttributeError(
                'Bad parent for : ' + module.package.name() + ' expected : ' + module.package.config().parent_name() + ' parent is : ' + self.__package.name())
        if module.package.config().has_parent_version() and module.package.config().parent_version() != self.__package.version():
            raise AttributeError(
                'Bad parent version for : ' + module.package.name() + ' expected : ' + module.package.config().parent_version() + ' parent have : ' + self.__package.version())

    def __load_modules(self):
        if not self.__package.config().has_modules():
            raise KeyError('No modules found for : ' + self.__package.name())

        module_path: str
        for module_path in self.__package.config().modules():
            path: Path = Path(self.__package.cwd / module_path)
            path.resolve()
            if not path.is_dir():
                raise FileNotFoundError('Module dir not found : ' + module_path)

            module: Module = Module(path)
            self.__check_parent_version(module)
            self.modules.append(module)

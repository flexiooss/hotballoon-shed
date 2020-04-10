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

    def __load_modules(self):
        if not self.__package.config().has_modules():
            raise KeyError('No modules found')

        module_path: str
        for module_path in self.__package.config().modules():
            path: Path = Path(self.__package.cwd / module_path)
            path.resolve()
            if not path.is_dir():
                raise FileNotFoundError('Module dir not found : ' + module_path)

            module: Module = Module(path)
            if not module.package.config().has_parent() or module.package.config().parent_name() != self.__package.name():
                raise NameError('Bad parent module for : ' + module.package.name())
            self.modules.append(module)

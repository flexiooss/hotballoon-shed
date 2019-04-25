from pathlib import Path
from typing import List

from cmd.package.PackageHandler import PackageHandler
from cmd.package.modules.Module import Module


class ModulesHandler:
    modules: List[Module]

    def __init__(self, package: PackageHandler) -> None:
        self.__package: PackageHandler = package
        self.modules: List[Module] = []
        self.__load_modules()

    def __load_modules(self):
        if not self.__package.config().has_modules():
            raise KeyError('No modules found')

        for name, module_path in self.__package.config().modules().items():
            path: Path = Path(self.__package.cwd / module_path)
            path.resolve()
            self.modules.append(Module(name, path))
from typing import Optional, Dict

from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class ApplyModulePeerDependencies:

    def __init__(self, package: HBShedPackageHandler,
                 dependencies: Optional[Dict[str, str]]) -> None:
        self.__package: HBShedPackageHandler = package
        self.__dependencies: Optional[Dict[str, str]] = dependencies

    def __apply(self):
        self.__package.set_peer_dependencies(self.__dependencies)
        self.__package.write()

    def __apply_modules_peer_dependencies(self):
        if self.__package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.__package)
            module: Module
            for module in modules.modules:
                ApplyModulePeerDependencies(
                    package=module.package,
                    dependencies=self.__dependencies
                ).process()

    def process(self):
        self.__apply()
        self.__apply_modules_peer_dependencies()

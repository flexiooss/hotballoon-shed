from pathlib import Path
from typing import Optional

from cmd.Tasks.Install.ModulePeerDependenciesProvisioner import ModulePeerDependenciesProvisioner
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class ApplyModulePeerDependencies:

    def __init__(self, root_package: Optional[HBShedPackageHandler], module: Module,
                 provisioner: ModulePeerDependenciesProvisioner) -> None:
        self.__root_package: Optional[HBShedPackageHandler] = root_package
        self.__module: Module = module
        self.__provisioner = provisioner

    def __apply_modules_peer_dependencies(self):
        if self.__module.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.__module.package)
            module: Module
            for module in modules.modules:
                ApplyModulePeerDependencies(
                    root_package=self.__root_package,
                    module=module,
                    provisioner=self.__provisioner
                ).process()

    def process(self):
        self.__provisioner.apply(self.__module.package)
        self.__apply_modules_peer_dependencies()

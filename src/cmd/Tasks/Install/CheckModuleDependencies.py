from pathlib import Path
from typing import Optional, List, Set, Dict

from cmd.Tasks.Install.ExternalModulesDependenciesProcessor import ExternalModulesDependenciesProcessor
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class CheckModuleDependencies:

    def __init__(self, root_package: Optional[HBShedPackageHandler], parent_package: Optional[HBShedPackageHandler],
                 module: Module, processor: ExternalModulesDependenciesProcessor) -> None:
        self.__root_package: Optional[HBShedPackageHandler] = root_package
        self.__parent_package: Optional[HBShedPackageHandler] = parent_package
        self.__module: Module = module
        self.__processor: ExternalModulesDependenciesProcessor = processor

    def __check_modules_dependencies(self):
        if self.__module.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.__module.package)
            module: Module
            for module in modules.modules:
                CheckModuleDependencies(
                    root_package=self.__root_package,
                    parent_package=self.__module.package,
                    module=module,
                    processor=self.__processor
                ).process()

    def __not_in_parent(self, dependencies: List[str], root_dep: Optional[Dict[str, str]]) -> Set[str]:
        ret: Set[str] = set([])

        name: str
        for name in dependencies:
            if root_dep is not None and root_dep.get(name) is None:
                if (self.__root_package.config().has_modules() and name not in self.__root_package.config().modules()) or not self.__root_package.config().has_modules():
                    ret.add(name)
        return ret

    def __check_dependencies_in_parent(self):
        if self.__module.package.config().has_dependencies():

            if not self.__root_package.has_dependencies():
                self.__processor.add_all(self.__module.package)
            else:
                external_dependencies: Set[str] = self.__not_in_parent(
                    self.__module.package.config().dependencies(),
                    self.__root_package.dependencies()
                )

                name: str
                for name in external_dependencies:
                    self.__processor.add(name)

    def __check_dev_dependencies_in_parent(self):
        if self.__module.package.config().has_dev_dependencies():
            external_dependencies: Set[str] = self.__not_in_parent(
                    self.__module.package.config().dev_dependencies(),
                    self.__root_package.dependencies()
                )

            external_dev_dependencies: Set[str] = self.__not_in_parent(
                    self.__module.package.config().dev_dependencies(),
                    self.__root_package.dev_dependencies()
                )

            name: str
            for name in external_dependencies:
                if name in external_dev_dependencies:
                    self.__processor.add(name)


    def __check_dependencies_local(self):
        if self.__module.package.has_dependencies():
            raise FileExistsError('Module can not have dependency at : ' + self.__module.package.name())

    def __check_dev_dependencies_local(self):
        if self.__module.package.has_dev_dependencies():
            raise FileExistsError('Module can not have devDependency at : ' + self.__module.package.name())

    def process(self):
        self.__check_dependencies_in_parent()
        self.__check_dev_dependencies_in_parent()
        self.__check_dependencies_local()
        self.__check_dev_dependencies_local()
        self.__check_modules_dependencies()

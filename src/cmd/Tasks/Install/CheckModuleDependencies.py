from pathlib import Path
from typing import Optional, List
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class CheckModuleDependencies:

    def __init__(self, root_package: Optional[HBShedPackageHandler], module: Module) -> None:
        self.__root_package: Optional[HBShedPackageHandler] = root_package
        self.__module: Module = module

    def __check_modules_dependencies(self):
        if self.__module.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.__module.package)
            module: Module
            for module in modules.modules:
                CheckModuleDependencies(
                    root_package=self.__root_package,
                    module=module
                ).process()

    def __check_dependencies_in_parent(self):
        if self.__module.package.config().has_dependencies():

            print('#### CHECK MODULES DEPENDENCIES : ' + self.__module.package.name())

            name: str
            if not self.__root_package.has_dependencies():
                raise FileNotFoundError('No dependencies found at : ' + self.__root_package.modules_path().as_posix())

            for name in self.__module.package.config().dependencies():
                if self.__root_package.dependencies().get(name) is None:
                    raise FileNotFoundError('parent should have dependency : ' + name)

    def __check_dev_dependencies_in_parent(self):
        if self.__module.package.config().has_dev_dependencies():

            print('#### CHECK MODULES DEV_DEPENDENCIES : ' + self.__module.package.name())

            name: str
            if not self.__root_package.has_dev_dependencies():
                raise FileNotFoundError(
                    'No devDependencies found at : ' + self.__root_package.modules_path().as_posix())

            for name in self.__module.package.config().dev_dependencies():
                if self.__root_package.dev_dependencies().get(name) is None and self.__root_package.dependencies().get(
                        name) is None:
                    raise FileNotFoundError('parent should have devDependency : ' + name)

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

from typing import Set, Dict, Optional

from cmd.Tasks.Install.PeerDependenciesWalkerProcessor import PeerDependenciesWalkerProcessor
from cmd.package.DependenciesWalker import DependenciesWalker
from cmd.package.DevDependenciesWalker import DevDependenciesWalker
from cmd.package.PackageHandler import PackageHandler


class ModulePeerDependenciesProvisioner:
    peer_dependencies: Optional[Dict[str, str]] = None

    def __init__(self, package: PackageHandler) -> None:
        self.__package: PackageHandler = package
        self.__processor: PeerDependenciesWalkerProcessor = PeerDependenciesWalkerProcessor()

    def count(self) -> int:
        return len(self.__processor.dependencies)

    def prepare(self):
        if self.__package.has_dependencies():
            name: str
            for name in self.__package.dependencies():
                DependenciesWalker(
                    target_package_name=name,
                    node_modules=self.__package.modules_path(),
                    processor=self.__processor

                ).process_all()

        if self.__package.has_dev_dependencies():
            name: str
            for name in self.__package.dev_dependencies():
                DevDependenciesWalker(
                    target_package_name=name,
                    node_modules=self.__package.modules_path(),
                    processor=self.__processor

                ).process()

    def __final_dependencies(self) -> Dict[str, str]:
        if self.peer_dependencies is None:
            self.peer_dependencies = {}

            name: str
            for name in self.__processor.dependencies:
                self.peer_dependencies[name] = "latest"

        return self.peer_dependencies

    def apply(self, package: PackageHandler):
        package.set_peer_dependencies(self.__final_dependencies())
        package.write()

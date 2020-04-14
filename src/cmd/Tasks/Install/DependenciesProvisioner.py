from typing import Set, Dict, Optional
import sys

from cmd.Tasks.Install.ParentDependenciesWalkerProcessor import ParentDependenciesWalkerProcessor
from cmd.Tasks.Install.ParentWalkerProcessor import ParentWalkerProcessor
from cmd.Tasks.Install.PeerDependenciesWalkerProcessor import PeerDependenciesWalkerProcessor
from cmd.package.DependenciesWalker import DependenciesWalker
from cmd.package.DevDependenciesWalker import DevDependenciesWalker
from cmd.package.PackageHandler import PackageHandler


class DependenciesProvisioner:
    peer_dependencies: Optional[Dict[str, str]] = None

    def __init__(self, package: PackageHandler, peer_processor: PeerDependenciesWalkerProcessor,
                 parent_processor: ParentWalkerProcessor,
                 parent_dependencies_processor: ParentDependenciesWalkerProcessor) -> None:
        self.__package: PackageHandler = package
        self.__peer_processor: PeerDependenciesWalkerProcessor = peer_processor
        self.__parent_processor: ParentWalkerProcessor = parent_processor
        self.__parent_dependencies_processor: ParentDependenciesWalkerProcessor = parent_dependencies_processor

    def __process_for_root_package(self):
        sys.stdout.write('*')
        sys.stdout.flush()
        self.__parent_processor.process(self.__package)
        self.__parent_dependencies_processor.process(self.__package)

    def process(self):
        self.__process_for_root_package()

        if self.__package.has_dependencies():
            name: str
            for name in self.__package.dependencies():
                sys.stdout.write('*')
                sys.stdout.flush()

                DependenciesWalker(
                    target_package_name=name,
                    node_modules=self.__package.modules_path(),
                    processors=[self.__peer_processor, self.__parent_processor, self.__parent_dependencies_processor]

                ).process_all()

        if self.__package.has_dev_dependencies():
            name: str
            for name in self.__package.dev_dependencies():
                sys.stdout.write('*')
                sys.stdout.flush()
                DevDependenciesWalker(
                    target_package_name=name,
                    node_modules=self.__package.modules_path(),
                    processors=[self.__peer_processor]

                ).process()

    # def apply(self, package: PackageHandler):
    #     package.set_peer_dependencies(self.__processor.dependencies)
    #     package.write()

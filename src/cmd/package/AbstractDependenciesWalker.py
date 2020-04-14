from __future__ import annotations
import abc
from pathlib import Path
from typing import List

from cmd.package.PackageHandler import PackageHandler
from cmd.package.WalkerProcessor import WalkerProcessor


class AbstractDependenciesWalker(abc.ABC):

    def __init__(self, target_package_name: str, node_modules: Path, processors: List[WalkerProcessor]) -> None:
        self.target_package_name: str = target_package_name
        self.node_modules: Path = node_modules
        self.processors: List[WalkerProcessor] = processors

    @abc.abstractmethod
    def process_all(self):
        pass

    def ensure_current_package(self) -> PackageHandler:
        target_path: Path = self.node_modules.joinpath(self.target_package_name)
        if not target_path.is_dir():
            raise FileNotFoundError(
                'Package : ' + self.target_package_name + ' not found at : ' + self.node_modules.as_posix())
        return PackageHandler(target_path)

    def process(self) -> PackageHandler:
        package: PackageHandler = self.ensure_current_package()

        processor: WalkerProcessor
        for processor in self.processors:
            processor.process(package)
        return package

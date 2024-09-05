from __future__ import annotations
import abc
import re
from pathlib import Path
from typing import List

from cmd.package.PackageHandler import PackageHandler
from cmd.package.WalkerProcessor import WalkerProcessor
from cmd.package.Version import Version


class AbstractDependenciesWalker(abc.ABC):

    def __init__(self, target_package_name: str, target_package_version: str, node_modules: Path,
                 processors: List[WalkerProcessor], prev_package: PackageHandler) -> None:
        self.target_package_name: str = target_package_name
        self.target_package_version: str = target_package_version
        self.node_modules: Path = node_modules
        self.processors: List[WalkerProcessor] = processors
        self.prev_package: PackageHandler = prev_package

    @abc.abstractmethod
    def process_all(self):
        pass

    def ensure_current_package(self) -> PackageHandler:
        target_path: Path = self.node_modules.joinpath(self.target_package_name)
        if not target_path.is_dir():
            raise FileNotFoundError(
                'Package : ' + self.target_package_name + ' not found at : ' + self.node_modules.as_posix())
        package: PackageHandler = PackageHandler(target_path)
        if re.match(re.compile(r'.*\.git$'), self.target_package_version) is None:
            if not Version(package.version()).satisfies(self.target_package_version):
                raise ImportError(
                    'Package : ' + self.prev_package.name() + ' version conflict with package : ' + self.target_package_name + ':' + self.target_package_version + ' version : ' + package.version() + ' already registered')
        return package

    def process(self) -> PackageHandler:
        package: PackageHandler = self.ensure_current_package()

        processor: WalkerProcessor
        for processor in self.processors:
            processor.process(package)
        return package

from pathlib import Path

from cmd.package.PackageHandler import PackageHandler
from cmd.package.WalkerProcessor import WalkerProcessor


class DevDependenciesWalker:
    def __init__(self, target_package_name: str, node_modules: Path, processor: WalkerProcessor) -> None:
        self.__target_package_name: str = target_package_name
        self.__node_modules: Path = node_modules
        self.__processor: WalkerProcessor = processor

    def __current_package(self) -> PackageHandler:
        target_path = self.__node_modules.joinpath(self.__target_package_name)
        if not target_path.is_dir():
            raise FileNotFoundError(
                'Package : ' + self.__target_package_name + ' not found at : ' + self.__node_modules.as_posix())
        return PackageHandler(target_path)

    def process_all(self):

        package: PackageHandler = self.process()
        if package.has_dev_dependencies():

            name: str
            version: str
            for name, version in package.dev_dependencies().items():
                DevDependenciesWalker(
                    target_package_name=name,
                    node_modules=self.__node_modules,
                    processor=self.__processor
                ).process_all()

    def process(self) -> PackageHandler:
        package: PackageHandler = self.__current_package()
        self.__processor.process(package)
        return package

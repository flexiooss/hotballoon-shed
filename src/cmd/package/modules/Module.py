from pathlib import Path

from cmd.package.PackageHandler import PackageHandler


class Module:
    name: str
    path: Path
    package: PackageHandler

    def __init__(self, name: str, path: Path) -> None:
        self.name = name
        self.path = path
        self.__load_package()

    def __load_package(self):
        self.package = PackageHandler(self.path)
        self.package.config()

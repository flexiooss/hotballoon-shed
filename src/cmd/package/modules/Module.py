from pathlib import Path

from cmd.package.HBShedPackageHandler import HBShedPackageHandler


class Module:
    name: str
    path: Path
    package: HBShedPackageHandler

    def __init__(self, path: Path) -> None:
        self.path = path
        self.__load_package()
        self.__ensure_name()

    def __load_package(self):
        self.package = HBShedPackageHandler(self.path)
        self.package.config()

    def __ensure_name(self):
        self.name = self.package.name()

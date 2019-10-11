from pathlib import Path

from cmd.package.HBShedPackageHandler import HBShedPackageHandler


class Module:
    name: str
    path: Path
    package: HBShedPackageHandler

    def __init__(self, name: str, path: Path) -> None:
        self.name = name
        self.path = path
        self.__load_package()
        self.__ensure_name()

    def __load_package(self):
        self.package = HBShedPackageHandler(self.path)
        self.package.config()

    def __ensure_name(self):
        if not self.name == self.package.data.get(HBShedPackageHandler.NAME_KEY):
            raise ValueError('Name module does not match with package.json : ' + self.name)

from __future__ import annotations

from typing import Optional

from cmd.package.Config import Config
from cmd.package.PackageHandler import PackageHandler


class HBShedPackageHandler(PackageHandler):
    HOTBALLOON_SHED_KEY: str = 'hotballoon-shed'

    @staticmethod
    def from_package_handler(package: PackageHandler) -> Optional[HBShedPackageHandler]:
        if package.data.get(HBShedPackageHandler.HOTBALLOON_SHED_KEY) is not None:
            return HBShedPackageHandler(package.cwd)
        return None

    def config(self) -> Config:
        if self.package_data[self.HOTBALLOON_SHED_KEY] is None:
            raise ValueError('No `hotballoon-shed` configuration founded')
        return Config(self.data[self.HOTBALLOON_SHED_KEY], self.cwd)

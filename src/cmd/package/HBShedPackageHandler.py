from __future__ import annotations
import json

from pathlib import Path

from cmd.package.Config import Config
from cmd.package.PackageHandler import PackageHandler


class HBShedPackageHandler(PackageHandler):
    HOTBALLOON_SHED_KEY: str = 'hotballoon-shed'

    def config(self) -> Config:
        if self.__data[self.HOTBALLOON_SHED_KEY] is None:
            raise ValueError('No `hotballoon-shed` configuration founded')
        return Config(self.__data[self.HOTBALLOON_SHED_KEY], self.cwd)

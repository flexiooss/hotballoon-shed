from __future__ import annotations
import json

from pathlib import Path

from cmd.package.Config import Config


class PackageHandler:
    FILE_NAME: str = 'package.json'
    NAME_KEY: str = 'name'
    VERSION_KEY: str = 'version'

    def __init__(self, cwd: Path):
        self.cwd: Path = cwd
        self.__file_path: Path = cwd / self.FILE_NAME
        self.__data: dict = self.__load_file()

    @property
    def data(self) -> dict:
        return self.__data

    def __load_file(self):
        if not self.__file_path.is_file():
            raise FileNotFoundError(self.__file_path)
        with self.__file_path.open() as json_data:
            d = json.load(json_data)
            return d

    def name(self) -> str:
        return self.__data[self.NAME_KEY]

    def version(self) -> str:
        return self.__data[self.VERSION_KEY]

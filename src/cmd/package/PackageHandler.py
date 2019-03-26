from __future__ import annotations
import json

from pathlib import Path


class PackageHandler:
    FILE_NAME: str = 'package.json'
    VERSION_KEY: str = 'version'
    HOTBALLOON_SHED_KEY: str = 'hotballoon-shed'

    def __init__(self, dir_path: Path):
        self.__file_path: Path = dir_path / self.FILE_NAME
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

    def version(self) -> str:
        return self.__data[self.VERSION_KEY]

    def config(self) -> dict:
        if self.__data[self.HOTBALLOON_SHED_KEY] is None:
            raise ValueError('No `hotballoon-shed` configuration founded')
        return self.__data[self.HOTBALLOON_SHED_KEY]

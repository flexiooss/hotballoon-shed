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
        self.file_path: Path = cwd / self.FILE_NAME
        self.package_data: dict = self.load_file()

    @property
    def data(self) -> dict:
        return self.package_data

    def load_file(self):
        if not self.file_path.is_file():
            raise FileNotFoundError(self.file_path)
        with self.file_path.open() as json_data:
            d = json.load(json_data)
            return d

    def name(self) -> str:
        return self.package_data[self.NAME_KEY]

    def version(self) -> str:
        return self.package_data[self.VERSION_KEY]

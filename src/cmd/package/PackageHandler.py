from __future__ import annotations
import json

from pathlib import Path

from cmd.package.Config import Config


class PackageHandler:
    FILE_NAME: str = 'package.json'
    NAME_KEY: str = 'name'
    VERSION_KEY: str = 'version'
    MODULES_PATH: str = 'node_modules'

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

    def modules_path(self) -> Path:
        modules_path: Path = self.cwd / self.MODULES_PATH

        if not modules_path.is_dir():
            raise FileNotFoundError('No ' + self.MODULES_PATH + ' found at : ' + modules_path.as_posix())

        return modules_path

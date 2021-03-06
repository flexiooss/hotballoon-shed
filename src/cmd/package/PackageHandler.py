from __future__ import annotations
import json

from pathlib import Path
from typing import Dict, Optional

from cmd.package.Config import Config


class PackageHandler:
    FILE_NAME: str = 'package.json'
    NAME_KEY: str = 'name'
    VERSION_KEY: str = 'version'
    MODULES_PATH: str = 'node_modules'
    PEER_DEPENDENCIES: str = 'peerDependencies'
    DEPENDENCIES: str = 'dependencies'
    DEV_DEPENDENCIES: str = 'devDependencies'

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

    def write(self):
        with self.file_path.open('w') as outfile:
            json.dump(self.data, outfile, indent=2)
            outfile.write("\n")

    def name(self) -> str:
        return self.package_data[self.NAME_KEY]

    def version(self) -> str:
        return self.package_data[self.VERSION_KEY]

    def has_peer_dependencies(self) -> bool:
        return self.data.get(self.PEER_DEPENDENCIES) is not None and len(self.peer_dependencies())

    def peer_dependencies(self) -> Optional[Dict[str, str]]:
        return self.data.get(self.PEER_DEPENDENCIES)

    def set_peer_dependencies(self, dependencies: Dict[str, str]):
        self.data[self.PEER_DEPENDENCIES] = dependencies

    def remove_peer_dependencies(self):
        self.data.pop(self.PEER_DEPENDENCIES, None)

    def has_dependencies(self) -> bool:
        return self.data.get(self.DEPENDENCIES) is not None and len(self.dependencies())

    def dependencies(self) -> Optional[Dict[str, str]]:
        return self.data.get(self.DEPENDENCIES)

    def has_dev_dependencies(self) -> bool:
        return self.data.get(self.DEV_DEPENDENCIES) is not None and len(self.dev_dependencies())

    def dev_dependencies(self) -> Optional[Dict[str, str]]:
        return self.data.get(self.DEV_DEPENDENCIES)

    def modules_path(self) -> Path:
        modules_path: Path = self.cwd / self.MODULES_PATH

        if not modules_path.is_dir():
            raise FileNotFoundError('No ' + self.MODULES_PATH + ' found at : ' + modules_path.as_posix())

        return modules_path

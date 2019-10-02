import os
import re
import shutil
from pathlib import Path
from subprocess import Popen
from typing import Optional

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class SelfInstall(Task):
    NAME = Tasks.SELF_INSTALL

    def __install_package(self):
        self.exec(['npm', 'install', '--no-package-lock', '--force'])

    def __install_generator(self):

        if not self.package.config().has_value_object_version():
            raise ValueError('No version found into package config')

        version: str = self.package.config().value_object_version()

        lib: Path = Path(self.cwd / Directories.LIB)
        lib.resolve()

        if lib.is_dir():
            shutil.rmtree(lib.as_posix())
            print('****     rm ' + lib.as_posix())
        else:
            lib.mkdir()
            print('****     create ' + lib.as_posix())

        generator: Path = Path(lib / Directories.VALUE_OBJECT_GENERATOR)
        generator.mkdir()
        print('****     create ' + generator.as_posix())

        print('****     install generator')

        self.exec([
            'mvn',
            'dependency:unpack-dependencies',
            '-DoutputDirectory=' + generator.as_posix(),
            '-DexcludeTransitive',
            '-DgeneratorVersion=' + version,
            '-DmarkersDirectory=' + lib.as_posix()
        ])

    def process(self):
        print('SELF_INSTALL')

        self.__install_package()
        self.__install_generator()

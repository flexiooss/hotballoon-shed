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

        self.exec([
            'mvn',
            '-Dartifact=org.codingmatters.value.objects:cdm-value-objects-js:' + version + ':zip:embedded',
            'dependency:get',
            '-DremoteRepositories=https://oss.sonatype.org/content/repositories/snapshots'
        ])

        self.exec(
            ['mvn', '-Dartifact=org.codingmatters.value.objects:cdm-value-objects-js:' + version + ':zip:embedded',
             'dependency:copy', '-DoutputDirectory=' + lib.as_posix()])

        generator: Path = Path(lib / Directories.VALUE_OBJECT_GENERATOR)
        generator.mkdir()
        print('****     create ' + generator.as_posix())

        archive: Optional[Path] = None

        for file in os.listdir(lib.as_posix()):
            if re.match(re.compile('^cdm-value-objects-js-.*-embedded\.zip$'), file) is not None:
                archive = Path(lib / file)

        if archive is None or not archive.is_file():
            raise FileNotFoundError('No `cdm-value-objects-js-*-embedded.zip` archive found')

        print('****     archive found : ' + archive.as_posix())

        child: Popen = Popen(['unzip', archive.as_posix(), '-d', Directories.VALUE_OBJECT_GENERATOR],
                             cwd=lib.as_posix())
        print('****     unzip ' + archive.as_posix() + ' into ' + Directories.VALUE_OBJECT_GENERATOR)

        child.communicate()

    def process(self):
        print('SELF_INSTALL')

        self.__install_package()
        self.__install_generator()

import os
import shutil
from pathlib import Path
from subprocess import Popen

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

        child: Popen = Popen(['unzip', 'cdm-value-objects-js-*-embedded.zip', '-d', Directories.VALUE_OBJECT_GENERATOR],
                             cwd=lib.as_posix())
        child.communicate()

    def process(self):
        print('SELF_INSTALL')

        self.__install_package()
        self.__install_generator()

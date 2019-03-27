import os
import shutil
from pathlib import Path
from subprocess import Popen

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class SelfInstall(Task):
    NAME = Tasks.SELF_INSTALL

    def __install_package(self, cwd: Path):

        package: Path = Path(cwd / 'package.json')
        package.resolve()

        if cwd.is_dir() and package.is_file():
            child: Popen = Popen(['npm', 'install', '--no-package-lock', '--force'], cwd=cwd.as_posix())
            child.communicate()
        else:
            raise FileNotFoundError('No package.json found')

    def __install_generator(self, cwd: Path):
        if not self.package.config().has_value_object_version():
            raise ValueError('No version found into package config')

        version: str = self.package.config().value_object_version()

        shutil.rmtree(Path(cwd / Directories.LIB).as_posix())

        self.exec([
            'mvn',
            '-Dartifact=org.codingmatters.value.objects:cdm-value-objects-js:' + version + ':zip:embedded',
            'dependency:get',
            '-DremoteRepositories=https://oss.sonatype.org/content/repositories/snapshots'
        ])

        lib: Path = Path(cwd / Directories.LIB)
        lib.resolve()

        self.exec(
            ['mvn', '-Dartifact=org.codingmatters.value.objects:cdm-value-objects-js:' + version + ':zip:embedded',
             'dependency:copy', '-DoutputDirectory=' + lib.as_posix()])

        child: Popen = Popen(['unzip', 'cdm-value-objects-js-*-embedded.zip', '-d', 'generator'], cwd=lib.as_posix())
        child.communicate()

    def process(self):
        print('SELF_INSTALL')

        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../..')
        p.resolve()

        self.__install_package(p)
        self.__install_generator(p)

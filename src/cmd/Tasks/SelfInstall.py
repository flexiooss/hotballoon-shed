import os
import stat
import re
import shutil
import sys
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Optional

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class SelfInstall(Task):
    NAME = Tasks.SELF_INSTALL

    def __install_package(self):
        self.exec(['npm', 'install', '--no-package-lock', '--force'])

        node_modules: Path = Path(self.cwd / Directories.NODE_MODULES)
        node_modules.resolve()

        if not node_modules.is_dir():
            raise ValueError('No node_modules found at : ' + node_modules.as_posix())
        st: os.stat_result = os.stat(node_modules)
        os.chmod(node_modules, st.st_mode | stat.S_IRGRP | stat.S_IROTH)

        for root, dirs, files in os.walk(node_modules):
            for name in files:
                file_name = os.path.join(root, name)
                st: os.stat_result = os.stat(file_name)
                os.chmod(file_name, st.st_mode | stat.S_IRGRP | stat.S_IROTH)
            for name in dirs:
                dir_name = os.path.join(root, name)
                st: os.stat_result = os.stat(dir_name)
                os.chmod(dir_name, st.st_mode | stat.S_IRGRP | stat.S_IROTH)

        print('****     chmod a+r recursively for : ' + node_modules.as_posix())

    def __install_generator(self):

        if not self.package.config().has_value_object_version():
            raise ValueError('No version found into package config')

        version: str = self.package.config().value_object_version()

        lib: Path = Path(self.cwd / Directories.LIB)
        lib.resolve()

        if lib.is_dir():
            shutil.rmtree(lib.as_posix())
            print('****     rm ' + lib.as_posix())

        lib.mkdir()
        print('****     create ' + lib.as_posix())

        generator: Path = Path(lib / Directories.VALUE_OBJECT_GENERATOR)
        generator.mkdir()
        print('****     create ' + generator.as_posix())

        print('****     install generator')

        p1 = Popen(
            [
                'mvn',
                'dependency:unpack-dependencies',
                '-DoutputDirectory=' + generator.as_posix(),
                '-DexcludeTransitive',
                '-DgeneratorVersion=' + version,
                '-DmarkersDirectory=' + lib.as_posix()
            ],
            cwd=self.cwd.as_posix()
        )

        p1.wait()

        code = p1.returncode
        if code != 0:
            sys.stderr.write("GENERATOR ****      Can't build generator" + "\n")
            sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
            sys.exit(code)

        generator_run: Path = Path(generator / 'run.sh')
        if not generator_run.is_file():
            raise ValueError('No generator runner found at : ' + generator_run.as_posix())

        st: os.stat_result = os.stat(generator_run)

        os.chmod(generator_run, st.st_mode | stat.S_IXGRP | stat.S_IXOTH)
        print('****     chmod a+x for : ' + generator_run.as_posix())

    def process(self):
        print('SELF_INSTALL')

        self.__install_package()
        self.__install_generator()

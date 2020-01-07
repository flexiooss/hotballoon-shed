import os
import shutil
import sys
from pathlib import Path
from subprocess import Popen

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Build(Task):
    NAME = Tasks.BUILD

    def process(self):
        print('**** BUILD : PROD : ' + self.package.name())

        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

        production_builder: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../build/' + self.package.config().builder() + '/production.js')
        production_builder.resolve()

        if not production_builder.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().builder())

        if not self.package.config().has_build_output():
            raise KeyError('No path for build found into `hotballoon-shed` configuration')

        verbose: str = '-v' if self.options.verbose is True else ''

        child: Popen = self.exec([
            'node',
            production_builder.as_posix(),
            verbose,
            ','.join([v.as_posix() for v in self.package.config().build_entries()]),
            self.package.config().build_html_template().as_posix(),
            self.package.config().build_output()
        ])
        code = child.returncode

        if code != 0:
            sys.stderr.write("BUILD FAIL" + "\n")
            sys.exit(code)

        print('**** BUILD : LIB : ' + self.package.name())

        lib_builder: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../build/' + self.package.config().builder() + '/lib.js')
        lib_builder.resolve()

        if not lib_builder.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().builder())

        if not self.package.config().has_build_output():
            raise KeyError('No path for build found into `hotballoon-shed` configuration')

        verbose: str = '-v' if self.options.verbose is True else ''

        child2: Popen = self.exec([
            'node',
            lib_builder.as_posix(),
            verbose,
            ','.join([v.as_posix() for v in self.package.config().build_entries()]),
            self.package.config().build_html_template().as_posix(),
            self.package.config().build_output()
        ])

        sys.exit(child2.returncode)

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
        print('BUILD : ' + self.package.name())

        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

        p: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../build/' + self.package.config().builder() + '/production.js')
        p.resolve()

        if not p.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().builder())

        if not self.package.config().has_build_output():
            raise KeyError('No path for build found into `hotballoon-shed` configuration')

        verbose: str = '-v' if self.options.verbose is True else ''

        child: Popen = self.exec([
            'node',
            p.as_posix(),
            verbose,
            ','.join([v.as_posix() for v in self.package.config().build_entries()]),
            self.package.config().build_html_template().as_posix(),
            self.package.config().build_output()
        ])
        sys.exit(child.returncode)

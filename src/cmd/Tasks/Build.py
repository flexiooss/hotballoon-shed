import os
import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Build(Task):
    NAME = Tasks.BUILD

    def process(self):
        print('BUILD')
        if self.package.config().get('builder') is None:
            raise KeyError('No builder found into `hotballoon-shed` configuration')
        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../build/' + self.package.config().get(
            'builder') + '/production.js')
        p.resolve()
        if not p.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().get('builder'))
        verbose: str = '-v' if self.options.verbose is True else ''
        self.exec(['node', p.as_posix(), verbose])

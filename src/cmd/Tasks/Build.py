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
        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../build/webpack4/production.js')
        p.resolve()
        print(p.as_posix())
        verbose: str = '-v' if self.options.verbose is True else ''
        self.exec(['node', p.as_posix(), verbose])

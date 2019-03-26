import os
import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Dev(Task):
    NAME = Tasks.DEV

    def process(self):
        print('DEV')
        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../build/webpack4/server.js')
        p.resolve()
        print(p.as_posix())
        verbose: str = '-v' if self.options.verbose is True else ''
        self.exec(['node', p.as_posix(), verbose])

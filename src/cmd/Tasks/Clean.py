import os
import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Clean(Task):
    NAME = Tasks.CLEAN

    def process(self):
        print('CLEAN')
        if Path(self.cwd.as_posix() + ('/' + Directories.NODE_MODULES)).is_dir():
            shutil.rmtree(Path(self.cwd.as_posix() + ('/' + Directories.NODE_MODULES)).as_posix())
            print('CLEAN : node_modules')

        if Path(self.cwd.as_posix() + ('/' + Directories.GENERATED)).is_dir():
            shutil.rmtree(Path(self.cwd.as_posix() + ('/' + Directories.GENERATED)).as_posix())
            print('CLEAN : generated')

        if Path(self.cwd.as_posix() + ('/' + Directories.DIST)).is_dir():
            shutil.rmtree(Path(self.cwd.as_posix() + ('/' + Directories.DIST)).as_posix())
            print('CLEAN : dist')

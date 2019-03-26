import os
from pathlib import Path

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Test(Task):
    NAME = Tasks.TEST

    def process(self):
        print('TEST')
        print(self.options.verbose)
        print(self.cwd.as_posix())
        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../build/test/test.js')
        p.resolve()
        print(p.as_posix())
        verbose: str = '-v' if self.options.verbose is True else ''
        self.exec(['node', p.as_posix(), verbose])

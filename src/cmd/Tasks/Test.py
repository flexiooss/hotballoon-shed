import os
from pathlib import Path

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Test(Task):
    NAME = Tasks.TEST

    def process(self):
        print('TEST')

        if self.package.config().get('test') is None:
            raise KeyError('No tester found into `hotballoon-shed` configuration')
        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../build/' + self.package.config().get(
            'test') + '/test.js')
        p.resolve()
        if not p.is_file():
            raise FileNotFoundError('No tester file found for this tester : ' + self.package.config().get('test'))
        verbose: str = '-v' if self.options.verbose is True else ''
        self.exec(['node', p.as_posix(), verbose])

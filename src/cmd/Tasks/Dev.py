import os
from pathlib import Path

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
import json


class Dev(Task):
    NAME = Tasks.DEV

    def process(self):
        print('DEV : ' + self.package.name())

        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

        p: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../build/' + self.package.config().builder() + '/server.js')
        p.resolve()

        if not p.is_file():
            raise FileNotFoundError('No server found for this builder : ' + self.package.config().builder())

        verbose: str = '-v' if self.options.verbose is True else ''
        self.exec([
            'node',
            p.as_posix(),
            verbose,
            ','.join([v.as_posix() for v in self.package.config().dev_entries()]),
            self.package.config().build_html_template().as_posix(),
            self.package.config().build_output().as_posix(),
            json.dumps(self.package.config().dev_server())
        ])

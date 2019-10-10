import os
from pathlib import Path

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
import json


class BrowserTest(Task):
    NAME = Tasks.DEV

    def process(self):
        print('BROWSER TEST : ' + self.package.name())
        if self.package.config().has_browser_test():

            if not self.package.config().has_builder():
                raise KeyError('No builder found into `hotballoon-shed` configuration')

            p: Path = Path(os.path.dirname(
                os.path.realpath(__file__)) + '/../../build/' + self.package.config().builder() + '/server.js')
            p.resolve()

            if not p.is_file():
                raise FileNotFoundError('No server found for this builder : ' + self.package.config().builder())

            template_html: Path = Path(os.path.dirname(
                os.path.realpath(__file__)) + '/../../build/' + self.package.config().builder() + '/index.html')
            template_html.resolve()

            if not template_html.is_file():
                raise FileNotFoundError('No html template found for this builder : ' + self.package.config().builder())

            if self.options.restrict is None:
                raise FileNotFoundError('No restrict given for find dev entry')

            entry: Path = Path(self.package.config().browser_test_dir() / self.options.restrict)
            entry.resolve()
            if not entry.is_file():
                raise FileNotFoundError('No entry found at : ' + entry.as_posix())

            temp_build: Path = Path(self.package.config().browser_test_dir() / 'tmp_dist')

            verbose: str = '-v' if self.options.verbose is True else ''
            self.exec([
                'node',
                p.as_posix(),
                verbose,
                ','.join([entry.as_posix()]),
                template_html.as_posix(),
                temp_build.as_posix(),
                json.dumps({'host': 'localhost'})
            ])
        else:
            print('BROWSER TEST NOT FOUND')

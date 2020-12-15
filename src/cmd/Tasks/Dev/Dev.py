import os
from pathlib import Path

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
import json
from cmd.Tasks.Dev.stack_server_config import stack_server_config
from cmd.Tasks.Dev.local_server_config import local_server_config


class Dev(Task):
    NAME = Tasks.DEV

    def __template_html(self) -> Path:
        if self.options.html_template is not None:
            html_template: Path = Path(self.package.cwd / self.options.html_template)
            html_template.resolve()
            if not html_template.is_file():
                raise FileNotFoundError('No HTML template found at : ' + html_template.as_posix())
            return html_template

        if self.package.config().has_build_html_template():
            return self.package.config().build_html_template()
        else:
            template_html: Path = Path(os.path.dirname(
                os.path.realpath(__file__)) + '/../../../build/' + self.package.config().builder() + '/index.html')
            template_html.resolve()

            if not template_html.is_file():
                raise FileNotFoundError('No html template found for this builder : ' + self.package.config().builder())
            return template_html

    def __build_output(self) -> Path:
        if self.package.config().has_build_output():
            return self.package.config().build_output()
        else:
            return Path(self.package.cwd / 'tmp_dist')

    def __node_server(self) -> Path:
        p: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../../build/' + self.package.config().builder() + '/server.js')
        p.resolve()
        if not p.is_file():
            raise FileNotFoundError('No server found for this builder : ' + self.package.config().builder())
        return p

    def __verbose(self) -> str:
        verbose: str = '-v' if self.options.verbose is True else ''
        return verbose

    def __ensure_builder(self):
        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

    def __entries(self) -> str:
        if self.options.entry is None:
            if not self.package.config().has_dev_entries():
                raise FileNotFoundError('No entry found')
            return ','.join([v.as_posix() for v in self.package.config().dev_entries()])
        else:
            entry: Path = Path(self.package.cwd / self.options.entry)
            entry.resolve()
            if not entry.is_file():
                raise FileNotFoundError('No entry found at : ' + entry.as_posix())
            return entry.as_posix()

    def __server_config(self) -> dict:
        if self.options.server_config is None:
            if self.package.config().has_dev_server():
                return self.package.config().dev_server()
        else:
            if self.options.server_config == 'local':
                if self.options.port is not None:
                    local_server_config['port'] = self.options.port
                return local_server_config
            if self.options.server_config == 'stack':
                return stack_server_config

        return {}

    def process(self):
        print('DEV : ' + self.package.name())

        self.__ensure_builder()

        self.exec([
            'node',
            self.__node_server().as_posix(),
            self.__verbose(),
            self.__entries(),
            self.__template_html().as_posix(),
            self.__build_output().as_posix(),
            json.dumps(self.__server_config())
        ])

import os
import shutil
import sys
from pathlib import Path
from subprocess import Popen

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.Tasks.Build.manifest_config import manifest_config
import json


class Build(Task):
    NAME = Tasks.BUILD

    def __build_app(self):
        print('****')
        print('**** BUILD APP : ' + self.package.name())
        print('****')

        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

        production_builder: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../../build/' + self.package.config().builder() + '/production.js')
        production_builder.resolve()

        if not production_builder.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().builder())

        if not self.package.config().has_build_output():
            raise KeyError('No path for build found into `hotballoon-shed` configuration')

        verbose: str = '-v' if self.options.debug else ''

        if self.package.config().has_application():
            manifest_config.update(self.package.config().application())

        html_template: Path = self.__resolve_html_template()

        child: Popen = self.exec([
            'node',
            production_builder.as_posix(),
            verbose,
            ','.join([v.as_posix() for v in self.package.config().build_entries()]),
            html_template.as_posix(),
            self.package.config().build_output(),
            json.dumps(manifest_config)
        ])
        code = child.returncode

        if code != 0:
            sys.stderr.write("BUILD APP FAIL" + "\n")
            raise ChildProcessError(code)

    def __resolve_html_template(self) -> Path:
        if self.package.config().has_html_template_name():
            return self.__tempate_path_for(self.package.config().html_template_name())
        elif self.package.config().has_build_html_template():
            return self.package.config().build_html_template()
        else:
            return self.__tempate_path_for('minimal')

    def __tempate_path_for(self, name: str) -> Path:
        template_html: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../../build/html/' + name + '/index.html')
        template_html.resolve()
        if not template_html.is_file():
            raise FileNotFoundError('No html template found for : ' + name)
        return template_html

    def __build_bundle(self):
        print('****')
        print('**** BUILD LIB BUNDLE : ' + self.package.name())
        print('****')
        lib_builder: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../../build/' + self.package.config().builder() + '/lib.js')
        lib_builder.resolve()
        if not lib_builder.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().builder())
        if not self.package.config().has_build_output():
            raise KeyError('No path for build found into `hotballoon-shed` configuration')
        verbose: str = '-v' if self.options.debug else ''

        html_template: Path = self.__resolve_html_template()

        child2: Popen = self.exec([
            'node',
            lib_builder.as_posix(),
            verbose,
            ','.join([v.as_posix() for v in self.package.config().build_entries()]),
            html_template.as_posix(),
            self.package.config().build_output()
        ])
        code = child2.returncode
        if code != 0:
            sys.stderr.write("BUILD LIB BUNDLE FAIL" + "\n")
            raise ChildProcessError(code)

    def process(self):
        self.__build_app()
        if self.options.bundle:
            self.__build_bundle()
        else:
            if self.options.debug:
                print('No bundle build required')

import os
import shutil
import sys
from pathlib import Path
from subprocess import Popen

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.OutputType import OutputType
import json
from typing import Optional


class Build(Task):
    NAME = Tasks.BUILD

    def __build_app(self):

        # print(self.package.config().build_entries())
        # exit(0)
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
            raise KeyError('No output path for build found into `hotballoon-shed` configuration')

        verbose: str = '-v' if self.options.debug else ''
        inspect: str = '1' if self.options.inspect else '0'


        html_template: Path = self.__resolve_html_template()

        entries: Dict = self.package.config().build_entries()
        # if(entries.has_key('service-worker')):
        #     del entries['service-worker']

        child: Popen = self.exec([
            'node',
            production_builder.as_posix(),
            verbose,
            json.dumps(entries),
            html_template.as_posix(),
            self.package.config().build_output(),
            inspect
        ])
        code = child.returncode

        if code != 0:
            sys.stderr.write("BUILD APP FAIL" + "\n")
            raise ChildProcessError(code)


    def __build_sw(self):
        print('****')
        print('**** BUILD APP SW: ' + self.package.name())
        print('****')

        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

        production_builder: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../../build/' + self.package.config().builder() + '/productionsw.js')
        production_builder.resolve()

        if not production_builder.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().builder())

        if not self.package.config().has_build_output():
            raise KeyError('No output path for build found into `hotballoon-shed` configuration')

        verbose: str = '-v' if self.options.debug else ''
        inspect: str = '1' if self.options.inspect else '0'

        entries: Dict = self.package.config().build_entries()
        if (entries.has_key('service-worker')):
            entry= entries['service-worker']

            html_template: Path = self.__resolve_html_template()

            child: Popen = self.exec([
                'node',
                production_builder.as_posix(),
                verbose,
                json.dumps(entry),
                html_template.as_posix(),
                self.package.config().build_output(),
                inspect
            ])
            code = child.returncode

            if code != 0:
                sys.stderr.write("BUILD APP SW FAIL" + "\n")
                raise ChildProcessError(code)


    def __build_app_debug(self):
        print('****')
        print('**** BUILD APP DEBUG : ' + self.package.name())
        print('****')

        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

        production_builder: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../../build/' + self.package.config().builder() + '/production_debug.js')
        production_builder.resolve()

        if not production_builder.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().builder())

        if not self.package.config().has_build_output():
            raise KeyError('No output path for build found into `hotballoon-shed` configuration')

        verbose: str = '-v' if self.options.debug else ''
        inspect: str = '1' if self.options.inspect else '0'


        html_template: Path = self.__resolve_html_template()

        child: Popen = self.exec([
            'node',
            production_builder.as_posix(),
            verbose,
            json.dumps(self.package.config().build_entries()),
            html_template.as_posix(),
            self.package.config().build_output()
        ])
        code = child.returncode

        if code != 0:
            sys.stderr.write("BUILD APP DEBUG FAIL" + "\n")
            raise ChildProcessError(code)

    def __resolve_html_template(self) -> Path:
        if self.package.config().has_build_html_template_name():
            return self.__tempate_path_for(self.package.config().build_html_template_name())
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
            raise KeyError('No output path for build found into `hotballoon-shed` configuration')
        verbose: str = '-v' if self.options.debug else ''

        html_template: Path = self.__resolve_html_template()

        child2: Popen = self.exec([
            'node',
            lib_builder.as_posix(),
            verbose,
            json.dumps(self.package.config().build_entries()),
            html_template.as_posix(),
            self.package.config().build_output()
        ])
        code = child2.returncode
        if code != 0:
            sys.stderr.write("BUILD LIB BUNDLE FAIL" + "\n")
            raise ChildProcessError(code)

    def process(self):
        output_type: Optional[OutputType] = OutputType.PRODUCTION.value
        if self.package.config().has_build_output_type():
            output_type = self.package.config().output_type()

        if output_type == OutputType.DEBUG.value:
            if self.options.debug:
                print('build output type: DEBUG')
            self.__build_app_debug()
            return
        elif output_type == OutputType.PRODUCTION.value:
            if self.options.debug:
                print('build output type: PRODUCTION')
            self.__build_app()
            return
        elif output_type == OutputType.BUNDLE.value:
            if self.options.debug:
                print('build output type: BUNDLE')
            self.__build_bundle()
            return
        else:
            if self.options.debug:
                print('EMPTY build : No build required')

import os
import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class GenerateSources(Task):
    NAME = Tasks.GENERATE_SOURCES

    def __modules_generate_sources(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                GenerateSources(self.options, module.package, module.package.cwd).process()

    def process(self):
        print('GENERATE SOURCES : ' + self.package.name())

        if self.package.config().has_value_object():

            if not self.package.config().has_value_object_extension():
                raise KeyError('No extension for value-object generator found into `hotballoon-shed` configuration')

            p: Path = self.cwd if not self.package.config().has_value_object_path() else self.package.config().value_object_path()
            p.resolve()

            if not p.is_dir():
                raise FileNotFoundError('No spec directory found')

            generator: Path = Path(os.path.dirname(os.path.realpath(
                __file__)) + '/../../../' + Directories.LIB + '/' + Directories.VALUE_OBJECT_GENERATOR + '/' + 'run.sh')
            generator.resolve()

            if not generator.is_file():
                raise FileNotFoundError('No value-object generator found')

            verbose: str = '-v' if self.options.verbose is True else ''

            print(generator.as_posix())

            self.exec([generator.as_posix(), p.as_posix(), Path(self.cwd / 'generated').as_posix(),
                       'io.flexio.' + self.package.name().replace('-', ''),
                       self.package.config().value_object_extension()])

        self.__modules_generate_sources()

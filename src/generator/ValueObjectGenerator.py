import os
import re
from pathlib import Path
from subprocess import Popen, PIPE

from typing import List, Optional

from cmd.Directories import Directories
from cmd.Options import Options
from cmd.package.HBShedPackageHandler import HBShedPackageHandler


class ValueObjectGenerator:

    def __init__(self, options: Options, package: Optional[HBShedPackageHandler], cwd: Path) -> None:
        self.options: Options = options
        self.package: Optional[HBShedPackageHandler] = package
        self.cwd: Path = cwd

    def __exec(self, args: List[str]) -> Popen:
        child: Popen = Popen(args, cwd=self.cwd.as_posix())
        child.communicate()
        return child

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.cwd.as_posix()).communicate()
        return self.__decode_stdout(stdout)

    def __decode_stdout(self, stdout) -> str:
        return stdout.strip().decode('utf-8')

    def generate(self):
        if self.package.config().has_value_object():

            if not self.package.config().has_value_object_extension():
                raise KeyError('No extension for value-object generator found into `hotballoon-shed` configuration')

            sources_path: Path = self.cwd if not self.package.config().has_value_object_path() else self.package.config().value_object_path()
            sources_path.resolve()

            if not sources_path.is_dir():
                raise FileNotFoundError('No spec directory found')

            generator_path: Path = Path(os.path.dirname(os.path.realpath(
                __file__)) + '/../../' + Directories.LIB + '/' + Directories.VALUE_OBJECT_GENERATOR + '/' + 'run.sh')
            generator_path.resolve()

            print(generator_path.as_posix())

            if not generator_path.is_file():
                raise FileNotFoundError('No value-object generator found')

            generator: str = generator_path.as_posix()
            sources: str = sources_path.as_posix()
            target: str = Path(self.cwd / Directories.GENERATED).as_posix()
            root_package: str = 'io.flexio.' + re.sub('^@flexio[-\w]+\/', '', self.package.name().replace('-', '_'))
            extension: str = self.package.config().value_object_extension()

            verbose: str = '-v' if self.options.verbose is True else ''

            print(' '.join([generator, sources, target, root_package, extension]))

            self.__exec([generator, sources, target, root_package, extension])

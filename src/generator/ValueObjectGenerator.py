import os
from pathlib import Path
from subprocess import Popen, PIPE

from typing import List, Optional

from cmd.Directories import Directories
from cmd.Options import Options
from cmd.package.PackageHandler import PackageHandler


class ValueObjectGenerator:

    def __init__(self, options: Options, package: Optional[PackageHandler], cwd: Path) -> None:
        self.options: Options = options
        self.package: Optional[PackageHandler] = package
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

            p: Path = self.cwd if not self.package.config().has_value_object_path() else self.package.config().value_object_path()
            p.resolve()

            if not p.is_dir():
                raise FileNotFoundError('No spec directory found')

            generator: Path = Path(os.path.dirname(os.path.realpath(
                __file__)) + '/../../' + Directories.LIB + '/' + Directories.VALUE_OBJECT_GENERATOR + '/' + 'run.sh')
            generator.resolve()

            print(generator.as_posix())

            if not generator.is_file():
                raise FileNotFoundError('No value-object generator found')

            verbose: str = '-v' if self.options.verbose is True else ''

            print(generator.as_posix())

            self.__exec([generator.as_posix(), p.as_posix(), Path(self.cwd / Directories.GENERATED).as_posix(),
                         'io.flexio.' + self.package.name().replace('-', '_'),
                         self.package.config().value_object_extension()])

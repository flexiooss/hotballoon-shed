import os
import shutil
from pathlib import Path
from subprocess import Popen, PIPE

from typing import List

from cmd.Directories import Directories
from cmd.Options import Options
from cmd.Subject import Subject


class CaseBuilder:

    def __init__(self, subject: Subject, options: Options, cwd: Path) -> None:
        self.__cwd: Path = cwd
        self.__subject: Subject = subject
        self.__options: options = options

    def __exec(self, args: List[str]) -> Popen:
        child: Popen = Popen(args, cwd=self.__cwd.as_posix())
        child.communicate()
        return child

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.__cwd.as_posix()).communicate()
        return self.__decode_stdout(stdout)

    def __decode_stdout(self, stdout) -> str:
        return stdout.strip().decode('utf-8')

    def process(self):
        if self.__subject == Subject.TEST:
            self.test_case()
        elif self.__subject == Subject.INSTALL:
            self.install_case()
        elif self.__subject == Subject.CLEAN:
            self.clean_case()
        elif self.__subject == Subject.DEV:
            self.dev_case()
        elif self.__subject == Subject.BUILD:
            self.build_case()
        else:
            raise ValueError('no subject for this command')


    def test_case(self):
        print('TEST')
        print(self.__options.verbose)
        print(self.__cwd.as_posix())
        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../build/test/test.js')
        p.resolve()
        print(p.as_posix())
        verbose: str = '-v' if self.__options.verbose is True else ''
        self.__exec(['node', p.as_posix(), verbose])

    def install_case(self):
        print('INSTALL')
        self.__exec(['npm', 'install', '--no-package-lock', '--force'])

    def clean_case(self):
        print('CLEAN')
        if Path(self.__cwd.as_posix()+('/'+Directories.NODE_MODULES )).is_dir():
            shutil.rmtree(Path(self.__cwd.as_posix()+('/'+Directories.NODE_MODULES)).as_posix())
            print('CLEAN : node_modules')

        if Path(self.__cwd.as_posix()+('/'+Directories.GENERATED)).is_dir():
            shutil.rmtree(Path(self.__cwd.as_posix()+('/'+Directories.GENERATED)).as_posix())
            print('CLEAN : generated')

        if Path(self.__cwd.as_posix()+('/'+Directories.DIST)).is_dir():
            shutil.rmtree(Path(self.__cwd.as_posix()+('/'+Directories.DIST)).as_posix())
            print('CLEAN : dist')

    def dev_case(self):
        print('DEV')
        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../build/webpack4/server.js')
        p.resolve()
        print(p.as_posix())
        verbose: str = '-v' if self.__options.verbose is True else ''
        self.__exec(['node', p.as_posix(), verbose])

    def build_case(self):
        print('BUILD')
        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../build/webpack4/production.js')
        p.resolve()
        print(p.as_posix())
        verbose: str = '-v' if self.__options.verbose is True else ''
        self.__exec(['node', p.as_posix(), verbose])

    def generate_case(self):
        # TODO
        pass

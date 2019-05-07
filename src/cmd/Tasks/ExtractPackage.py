import os
import shutil
import sys
from pathlib import Path
from subprocess import Popen

from cmd.Tasks.CleanBuild import CleanBuild
from cmd.Tasks.CleanDependencies import CleanDependencies
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.PackageHandler import PackageHandler


class ExtractPackage(Task):
    NAME = Tasks.EXTRACT_PACKAGE
    target_path: Path = None
    target_package: PackageHandler = None

    def __ensure_target_path(self):
        if self.options.target_path is None:
            raise FileNotFoundError('No target path for extract this package')
        else:
            self.target_path = Path(self.options.target_path)
            if self.target_path.is_dir():
                raise FileExistsError('Target path option already exists')

    def __copy_to_target(self):
        shutil.copytree(self.cwd.as_posix(), self.target_path.as_posix())

    def __set_package(self):
        self.target_package = PackageHandler(self.target_path)

    def __rm_tests(self):
        if self.target_package.config().has_test():
            if self.target_package.config().test_dir().is_dir():
                shutil.rmtree(self.target_package.config().test_dir().as_posix())
                print('****     CLEAN : tests')

    def __rm_git(self):
        if Path(self.target_path.as_posix() + '/.git').is_dir():
            shutil.rmtree(Path(self.target_path.as_posix() + '/.git').as_posix())
            print('****     CLEAN : git')
        if Path(self.target_path.as_posix() + '/.gitignore').is_file():
            os.remove(Path(self.target_path.as_posix() + '/.gitignore').as_posix())
            print('****     CLEAN : .gitignore')

    def __rm_dependencies(self):
        CleanDependencies(self.options, self.target_package, self.target_path).process()

    def __rm_build(self):
        CleanBuild(self.options, self.target_package, self.target_path).process()

    def __rm_poom_ci(self):
        if Path(self.target_path.as_posix() + '/.poom-ci-pipeline').is_dir():
            shutil.rmtree(Path(self.target_path.as_posix() + '/.poom-ci-pipeline').as_posix())
            print('****     CLEAN : .poom-ci-pipeline')

        if Path(self.target_path.as_posix() + '/poom-ci-pipeline.yaml').is_file():
            os.remove(Path(self.target_path.as_posix() + '/poom-ci-pipeline.yaml').as_posix())
            print('****     CLEAN : poom-ci-pipeline.yaml')

    def process(self):
        print('****')
        print(self.NAME.value + ' : ' + self.package.name())

        self.__ensure_target_path()
        self.__copy_to_target()
        self.__set_package()
        self.__rm_tests()
        self.__rm_dependencies()
        self.__rm_build()
        self.__rm_git()
        self.__rm_poom_ci()

        print(self.package.name() + ' extracted to : ' + self.target_path.as_posix())
        print('****')

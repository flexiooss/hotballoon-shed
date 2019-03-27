from pathlib import Path
from typing import List, Optional
from cmd.Options import Options
from cmd.Tasks.Build import Build
from cmd.Tasks.Clean import Clean
from cmd.Tasks.Dev import Dev
from cmd.Tasks.Generate import Generate
from cmd.Tasks.Install import Install
from cmd.Tasks.SelfInstall import SelfInstall
from cmd.Tasks.Tasks import Tasks
from cmd.Tasks.Test import Test
from cmd.package.PackageHandler import PackageHandler


class TaskBuilder:
    __package: Optional[PackageHandler] = None

    def __init__(self, tasks: List[Tasks], options: Options, cwd: Path) -> None:
        self.__cwd: Path = cwd
        self.__tasks: List[Tasks] = tasks
        self.__options: Options = options
        print(self.__package.config())

    def __ensure_load_package(self):
        self.__package = PackageHandler(self.__cwd)
        self.package.config()

    def process(self):
        task: Tasks
        for task in self.__tasks:
            if task == Tasks.TEST:
                self.__ensure_load_package()
                Test(self.__options, self.__package, self.__cwd).process()
            elif task == Tasks.SELF_INSTALL:
                SelfInstall(self.__options, self.__package, self.__cwd).process()
            elif task == Tasks.INSTALL:
                self.__ensure_load_package()
                Install(self.__options, self.__package, self.__cwd).process()
            elif task == Tasks.CLEAN:
                self.__ensure_load_package()
                Clean(self.__options, self.__package, self.__cwd).process()
            elif task == Tasks.DEV:
                self.__ensure_load_package()
                Dev(self.__options, self.__package, self.__cwd).process()
            elif task == Tasks.BUILD:
                self.__ensure_load_package()
                Build(self.__options, self.__package, self.__cwd).process()
            elif task == Tasks.GENERATE:
                self.__ensure_load_package()
                Generate(self.__options, self.__package, self.__cwd).process()
            else:
                raise ValueError('no tasks for this command')

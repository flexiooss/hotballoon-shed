import os
from pathlib import Path
from typing import List, Optional
from cmd.Options import Options
from cmd.Tasks.Build import Build
from cmd.Tasks.Clean import Clean
from cmd.Tasks.CleanDependencies import CleanDependencies
from cmd.Tasks.CleanSources import CleanSources
from cmd.Tasks.CleanBuild import CleanBuild
from cmd.Tasks.Dev import Dev
from cmd.Tasks.ExtractPackage import ExtractPackage
from cmd.Tasks.GenerateSources import GenerateSources
from cmd.Tasks.Install import Install
from cmd.Tasks.Publish import Publish
from cmd.Tasks.SelfInstall import SelfInstall
from cmd.Tasks.SetFlexioRegistry import SetFlexioRegistry
from cmd.Tasks.Tasks import Tasks
from cmd.Tasks.Test import Test
from cmd.Tasks.BrowserTest import BrowserTest
from cmd.package.PackageHandler import PackageHandler


class TaskBuilder:
    __package: Optional[PackageHandler] = None

    def __init__(self, tasks: List[Tasks], options: Options, cwd: Path) -> None:
        self.__cwd: Path = cwd
        self.__tasks: List[Tasks] = tasks
        self.__options: Options = options

    def __ensure_load_package(self):
        self.__package = PackageHandler(self.__cwd)
        self.__package.config()

    def process(self):
        task: Tasks
        for task in self.__tasks:
            if task == Tasks.TEST:
                self.__ensure_load_package()
                Test(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.SELF_INSTALL:
                p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../..')
                p.resolve()
                SelfInstall(self.__options, PackageHandler(p), p).process()

            elif task == Tasks.INSTALL:
                self.__ensure_load_package()
                Install(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.CLEAN:
                self.__ensure_load_package()
                Clean(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.CLEAN_DEPENDENCIES:
                self.__ensure_load_package()
                CleanDependencies(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.CLEAN_SOURCES:
                self.__ensure_load_package()
                CleanSources(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.CLEAN_BUILD:
                self.__ensure_load_package()
                CleanBuild(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.DEV:
                self.__ensure_load_package()
                Dev(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.BROWSER_TEST:
                self.__ensure_load_package()
                BrowserTest(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.EXTRACT_PACKAGE:
                self.__ensure_load_package()
                ExtractPackage(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.BUILD:
                self.__ensure_load_package()
                Build(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.GENERATE_SOURCES:
                self.__ensure_load_package()
                GenerateSources(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.SET_FLEXIO_REGISTRY:
                self.__ensure_load_package()
                SetFlexioRegistry(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.PUBLISH:
                self.__ensure_load_package()
                Publish(self.__options, self.__package, self.__cwd).process()


            else:
                raise ValueError('no tasks for this command')

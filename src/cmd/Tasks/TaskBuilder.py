import os
from pathlib import Path
from typing import List, Optional
from cmd.Options import Options
from cmd.Tasks.Build.Build import Build
from cmd.Tasks.Clean.Clean import Clean
from cmd.Tasks.Clean.CleanDependenciesDir import CleanDependenciesDir
from cmd.Tasks.Clean.CleanSources import CleanSources
from cmd.Tasks.Clean.CleanBuild import CleanBuild
from cmd.Tasks.Dev.Dev import Dev
from cmd.Tasks.ExtractPackage.ExtractPackage import ExtractPackage
from cmd.Tasks.GenerateSources import GenerateSources
from cmd.Tasks.Install.Install import Install
from cmd.Tasks.Publish import Publish
from cmd.Tasks.SelfInstall import SelfInstall
from cmd.Tasks.SetFlexioRegistry import SetFlexioRegistry
from cmd.Tasks.Tasks import Tasks
from cmd.Tasks.Test import Test
from cmd.Tasks.BrowserTest import BrowserTest
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.PackageHandler import PackageHandler


class TaskBuilder:
    __package: Optional[PackageHandler] = None

    def __init__(self, tasks: List[Tasks], options: Options, cwd: Path) -> None:
        self.__cwd: Path = cwd
        self.__tasks: List[Tasks] = tasks
        self.__options: Options = options

    def __ensure_load_hb_package(self):
        self.__package = HBShedPackageHandler(self.__cwd)
        self.__package.config()

    def __ensure_load_package(self):
        self.__package = PackageHandler(self.__cwd)

    def process(self):
        task: Tasks
        for task in self.__tasks:
            if task == Tasks.TEST:
                self.__ensure_load_hb_package()
                Test(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.SELF_INSTALL:
                p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../..')
                p.resolve()
                SelfInstall(self.__options, HBShedPackageHandler(p), p).process()

            elif task == Tasks.INSTALL:
                self.__ensure_load_hb_package()
                Install(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.CLEAN:
                self.__ensure_load_hb_package()
                Clean(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.CLEAN_DEPENDENCIES_DIR:
                self.__ensure_load_hb_package()
                CleanDependenciesDir(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.CLEAN_SOURCES:
                self.__ensure_load_hb_package()
                CleanSources(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.CLEAN_BUILD:
                self.__ensure_load_hb_package()
                CleanBuild(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.DEV:
                self.__ensure_load_hb_package()
                Dev(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.BROWSER_TEST:
                self.__ensure_load_hb_package()
                BrowserTest(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.EXTRACT_PACKAGE:
                self.__ensure_load_hb_package()
                ExtractPackage(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.BUILD:
                self.__ensure_load_hb_package()
                Build(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.GENERATE_SOURCES:
                self.__ensure_load_hb_package()
                GenerateSources(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.SET_FLEXIO_REGISTRY:
                self.__ensure_load_hb_package()
                SetFlexioRegistry(self.__options, self.__package, self.__cwd).process()

            elif task == Tasks.PUBLISH:
                self.__ensure_load_package()
                Publish(self.__options, self.__package, self.__cwd).process()


            else:
                raise ValueError('no tasks for this command')

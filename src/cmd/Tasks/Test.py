import os
import sys
from pathlib import Path
from subprocess import Popen
import shutil

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class Test(Task):
    NAME = Tasks.TEST

    def __modules_test(self):
        if self.package.config().has_modules():
            print('TEST for modules')
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                Test(self.options, module.package, module.package.cwd).process()

    def __ensure_clean(self):
        if self.options.clean is not None:
            cache: Path = Path('/tmp/hotballoon-shed/cache')
            if cache.is_dir():
                shutil.rmtree(cache.as_posix())
                print('**** CLEAN TEST CACHE')

    def __ensure_builder(self):
        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

    def process(self):
        if self.package.config().has_test():
            self.__ensure_builder()
            self.__ensure_clean()
            print('TEST : ' + self.package.name())

            if not self.package.config().has_tester():
                raise KeyError('No tester found into `hotballoon-shed` configuration')

            tester: Path = Path(os.path.dirname(
                os.path.realpath(__file__)) + '/../../build/' + self.package.config().tester() + '/test.js')
            tester.resolve()

            if not tester.is_file():
                raise FileNotFoundError('No tester file found for this tester : ' + self.package.config().tester())

            verbose: str = '-v' if self.options.debug else ''
            restrict: str = self.options.restrict if self.options.restrict is not None else ''
            source_map:str = '1' if self.options.source_map else '0'
            child: Popen = self.exec(
                ['node', tester.as_posix(), self.package.config().test_dir().as_posix(), verbose, restrict,source_map, self.package.config().builder()])

            if child.returncode > 0:
                sys.exit(child.returncode)
        else:
            print('NO TEST : ' + self.package.name())

        if self.options.module_only is not True:
            self.__modules_test()

import os
import sys
from pathlib import Path
from subprocess import Popen

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class Test(Task):
    NAME = Tasks.TEST

    def __modules_test(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                Test(self.options, module.package, module.package.cwd).process()

    def process(self):
        print('TEST : ' + self.package.name())
        if self.package.config().has_test():

            if not self.package.config().has_tester():
                raise KeyError('No tester found into `hotballoon-shed` configuration')

            p: Path = Path(os.path.dirname(
                os.path.realpath(__file__)) + '/../../build/' + self.package.config().tester() + '/test.js')
            p.resolve()

            if not p.is_file():
                raise FileNotFoundError('No tester file found for this tester : ' + self.package.config().tester())

            verbose: str = '-v' if self.options.verbose is True else ''
            child: Popen = self.exec(['node', p.as_posix(), self.package.config().test_dir().as_posix(), verbose])
            if child.returncode > 0:
                sys.exit(child.returncode)

        self.__modules_test()

import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class CleanTests(Task):
    NAME = Tasks.CLEAN_TESTS

    def __modules_clean(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                CleanTests(self.options, module.package, module.package.cwd).process()

    def process(self):
        if self.package.config().has_test():
            if self.package.config().test_dir().is_dir():
                shutil.rmtree(self.package.config().test_dir().as_posix())
                print('CLEAN TESTS : ' + self.package.name())

        self.__modules_clean()

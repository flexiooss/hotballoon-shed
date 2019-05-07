import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class CleanBuild(Task):
    NAME = Tasks.CLEAN_BUILD

    def __modules_clean(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                CleanBuild(self.options, module.package, module.package.cwd).process()

    def process(self):
        print('CLEAN BUILD: ' + self.package.name())

        if self.package.config().has_build_output() and self.package.config().build_output().is_dir():
            shutil.rmtree(self.package.config().build_output().as_posix())
            print('****     CLEAN : build output')

        self.__modules_clean()

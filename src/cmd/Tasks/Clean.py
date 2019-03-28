import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class Clean(Task):
    NAME = Tasks.CLEAN

    def __modules_clean(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                Clean(self.options, module.package, module.package.cwd).process()

    def process(self):
        print('CLEAN : ' + self.package.name())
        if Path(self.cwd.as_posix() + ('/' + Directories.NODE_MODULES)).is_dir():
            shutil.rmtree(Path(self.cwd.as_posix() + ('/' + Directories.NODE_MODULES)).as_posix())
            print('****     CLEAN : node_modules')

        if Path(self.cwd.as_posix() + ('/' + Directories.GENERATED)).is_dir():
            shutil.rmtree(Path(self.cwd.as_posix() + ('/' + Directories.GENERATED)).as_posix())
            print('****     CLEAN : generated')

        if self.package.config().has_build_output() and self.package.config().build_output().is_dir():
            shutil.rmtree(self.package.config().build_output().as_posix())
            print('****     CLEAN : build output')

        self.__modules_clean()

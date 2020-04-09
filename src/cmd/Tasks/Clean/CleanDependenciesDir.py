import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class CleanDependenciesDir(Task):
    NAME = Tasks.CLEAN_DEPENDENCIES

    def __modules_clean(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                CleanDependenciesDir(self.options, module.package, module.package.cwd).process()

    def process(self):
        print('CLEAN DEPENDENCIES DIR : ' + self.package.name())
        if Path(self.cwd.as_posix() + ('/' + Directories.NODE_MODULES)).is_dir():
            shutil.rmtree(Path(self.cwd.as_posix() + ('/' + Directories.NODE_MODULES)).as_posix())
            print('****     CLEAN : node_modules')

        if self.options.module_only is not True:
            self.__modules_clean()

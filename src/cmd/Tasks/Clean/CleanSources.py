import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class CleanSources(Task):
    NAME = Tasks.CLEAN_SOURCES

    def __modules_clean(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                CleanSources(self.options, module.package, module.package.cwd).process()

    def process(self):
        print('CLEAN SOURCES: ' + self.package.name())

        if Path(self.cwd.as_posix() + ('/' + Directories.GENERATED)).is_dir():
            shutil.rmtree(Path(self.cwd.as_posix() + ('/' + Directories.GENERATED)).as_posix())
            print('****     CLEAN : generated')

        self.__modules_clean()

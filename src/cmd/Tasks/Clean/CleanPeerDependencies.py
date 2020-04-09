import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class CleanPeerDependencies(Task):
    NAME = Tasks.CLEAN_PEER_DEPENDENCIES

    def __modules_clean(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                CleanPeerDependencies(self.options, module.package, module.package.cwd).process()

    def process(self):
        if self.package.has_peer_dependencies():
            self.package.set_peer_dependencies({})
            self.package.write()

        if self.options.module_only is not True:
            self.__modules_clean()

from pathlib import Path
from typing import Optional

from cmd.Options import Options
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.PackageHandler import PackageHandler
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class Install(Task):
    NAME = Tasks.INSTALL

    def __init__(self, options: Options, package: Optional[PackageHandler], cwd: Path,
                 node_modules: Optional[Path] = None) -> None:
        super().__init__(options, package, cwd)
        self.__node_modules: Optional[Path] = node_modules
        self.__ensure_node_modules()

    def __ensure_node_modules(self):
        if self.__node_modules is None:
            self.__node_modules = self.cwd

    def __modules_install(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                Install(self.options, module.package, module.package.cwd, self.__node_modules).process()

    def process(self):
        print('INSTALL : ' + self.package.name())
        self.exec(['npm', 'install', self.__node_modules.as_posix(), '--no-package-lock', '--force'])

        self.__modules_install()

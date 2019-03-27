from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class Install(Task):
    NAME = Tasks.INSTALL

    def __modules_install(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                Install(self.options, module.package, module.package.cwd).process()

    def process(self):
        print('INSTALL : ' + self.package.name())
        self.exec(['npm', 'install', '--no-package-lock', '--force'])

        self.__modules_install()


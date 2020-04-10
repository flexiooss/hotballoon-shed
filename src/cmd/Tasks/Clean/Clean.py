from cmd.Tasks.Clean.CleanBuild import CleanBuild
from cmd.Tasks.Clean.CleanDependenciesDir import CleanDependenciesDir
from cmd.Tasks.Clean.CleanSources import CleanSources
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
        CleanBuild(self.options, self.package, self.cwd).process()
        CleanDependenciesDir(self.options, self.package, self.cwd).process()
        CleanSources(self.options, self.package, self.cwd).process()

        # if self.options.module_only is not True:
        #   self.__modules_clean()


from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler
from generator.ValueObjectGenerator import ValueObjectGenerator


class GenerateSources(Task):
    NAME = Tasks.GENERATE_SOURCES

    def __modules_generate_sources(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module

            print('#### #### ' + str(len(modules.modules)) + ' Modules found ')
            for module in modules.modules:
                GenerateSources(self.options, module.package, module.package.cwd).process()

    def process(self):

        ValueObjectGenerator(self.options, self.package, self.cwd).generate()

        if self.options.module_only is not True:
            self.__modules_generate_sources()

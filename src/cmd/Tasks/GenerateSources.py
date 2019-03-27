import os
import shutil
from pathlib import Path

from cmd.Directories import Directories
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
            for module in modules.modules:
                GenerateSources(self.options, module.package, module.package.cwd).process()

    def process(self):
        print('GENERATE SOURCES : ' + self.package.name())

        ValueObjectGenerator(self.options, self.package, self.cwd).generate()

        self.__modules_generate_sources()

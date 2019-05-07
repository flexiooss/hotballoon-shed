from cmd.Tasks.CleanBuild import CleanBuild
from cmd.Tasks.CleanDependencies import CleanDependencies
from cmd.Tasks.CleanSources import CleanSources
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Clean(Task):
    NAME = Tasks.CLEAN

    def process(self):
        print('CLEAN : ' + self.package.name())
        CleanBuild(self.options, self.package, self.cwd).process()
        CleanDependencies(self.options, self.package, self.cwd).process()
        CleanSources(self.options, self.package, self.cwd).process()

import os
from pathlib import Path

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Install(Task):
    NAME = Tasks.INSTALL

    def process(self):
        print('INSTALL')
        self.exec(['npm', 'install', '--no-package-lock', '--force'])


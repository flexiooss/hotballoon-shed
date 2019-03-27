import os
import shutil
from pathlib import Path

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class GenerateSources(Task):
    NAME = Tasks.GENERATE_SOURCES

    def process(self):
        print('GENERATE_SOURCES')

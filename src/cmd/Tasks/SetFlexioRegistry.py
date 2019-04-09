import os
import shutil
from pathlib import Path
from subprocess import Popen

from typing import List

from cmd.Directories import Directories
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class SetFlexioRegistry(Task):
    NAME = Tasks.SET_FLEXIO_REGISTRY

    def __set_flexio_registry(self):
        scopes: List[str] = ['@flexio-oss', '@flexio-services', '@flexio-components', '@flexio-vues', '@flexio-styles']

        for scope in scopes:
            self.exec(['npm', 'config', 'set', scope + ':registry https://verdaccio.ci.flexio.io'])

    def process(self):
        print('SET FLEXIO REGISTRY')

        self.__set_flexio_registry()

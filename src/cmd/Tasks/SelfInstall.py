import os
from pathlib import Path
from subprocess import Popen

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class SelfInstall(Task):
    NAME = Tasks.SELF_INSTALL

    def process(self):
        print('SELF_INSTALL')

        p: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../..')
        p.resolve()

        package: Path = Path(os.path.dirname(os.path.realpath(__file__)) + '/../../../package.json')
        package.resolve()
        if p.is_dir() and package.is_file():
            print(p.as_posix())
            child: Popen = Popen(['npm', 'install', '--no-package-lock', '--force'], cwd=p.as_posix())
            child.communicate()
        else:
            raise FileNotFoundError('No package.json found')

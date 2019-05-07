import os
import sys
from pathlib import Path
from subprocess import Popen, PIPE

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler


class Publish(Task):
    NAME = Tasks.PUBLISH

    def process(self):
        print('PUBLISH : ' + self.package.name())

        if self.options.registry is None or self.options.email is None or self.options.password is None or self.options.username is None:
            raise ValueError('Publish need registry, username, password, email')

        print("deploying JS package in " + self.cwd.as_posix())
        bash = Popen(["bash"], stdin=PIPE, stdout=PIPE, stderr=PIPE,
                     shell=True, cwd=self.cwd.as_posix())
        commands = """\
           npm-cli-login -u """ + self.options.username + """ -p """ + self.options.password + """ -e  """ + self.options.email + """" -r """ + self.options.registry + """
           npm publish --registry """ + self.options.registry + """ -f
           exit 0
           """
        bash.stdin.write(commands)
        bash.stdin.flush()
        bash.wait()
        code = bash.returncode
        if code != 0:
            sys.stderr.write("Command terminated with wrong status code: " + code)
            sys.stderr.write("Can't upload JS package: " + self.cwd.as_posix())
            result = bash.stdout.read()
            print("OUT: " + result)
            result = bash.stderr.read()
            print("ERR: " + result)
            sys.exit(code)

        print("Js package uploaded: " + self.cwd.as_posix())

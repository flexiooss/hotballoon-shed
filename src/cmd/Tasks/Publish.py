import glob
import os
import sys
from pathlib import Path
from subprocess import Popen, PIPE

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Publish(Task):
    NAME = Tasks.PUBLISH

    def get_last_file(self, file_pattern: str) -> str:
        list_of_files = glob.glob(file_pattern)
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file

    def print_last_lines(self, filename: str, no_of_lines: int = 1):
        file = open(filename, 'r')
        lines = file.readlines()
        last_lines = lines[-no_of_lines:]
        for line in last_lines:
            print(line)
        file.close()

    def print_last_npm_logs(self, lines: int = 50):
        npm_log_dir: Path = Path(Path().home() / '.npm/_logs')
        if npm_log_dir.is_dir():
            logs: Path = Path(self.get_last_file(npm_log_dir.as_posix() + '/*.log'))
            if logs.is_file():
                self.print_last_lines(logs.as_posix(), lines)
            else:
                print('No npm file log found')
        else:
            print('No npm dif log found at ' + npm_log_dir.as_posix())

    def process(self):
        print('PUBLISH : ' + self.package.name())

        if self.options.registry is None or self.options.email is None or self.options.password is None or self.options.username is None:
            raise ValueError('Publish need registry, username, password, email')

        print('****     registry : ' + self.options.registry)
        print('****     username : ' + self.options.username)
        print('****     email : ' + self.options.email)
        print('****     sources : ' + self.cwd.as_posix())

        print("deploying JS package in " + self.cwd.as_posix())

        print('****     ****    LOGIN')
        p1 = Popen(
            ['npm-cli-login', '-u', self.options.username, '-p', self.options.password, '-e', self.options.email, '-r',
             self.options.registry],
            stdout=PIPE,
            cwd=self.cwd.as_posix()
        )

        p1.wait()
        code = p1.returncode
        if code != 0:
            sys.stderr.write("LOGIN ****      Can't upload JS package: " + self.cwd.as_posix() + "\n")
            self.print_last_npm_logs(50)
            sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
            sys.exit(code)
        print('****     ****    LOGGED')

        print('****     ****    UNPUBLISH')
        p2 = Popen(
            ['npm', 'unpublish', self.package.name() + '@' + self.package.version(), '--registry',
             self.options.registry],
            stdin=p1.stdout,
            stdout=PIPE,
            cwd=self.cwd.as_posix()
        )

        p2.wait()
        code = p2.returncode

        if code != 0:
            sys.stderr.write("UNPUBLISH ****      Can't upload JS package: " + self.cwd.as_posix() + "\n")
            self.print_last_npm_logs(50)
            sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
            sys.exit(code)

        print('****     ****    UNPUBLISHED')

        print('****     ****    PUBLISH')
        p3 = Popen(
            ['npm', 'publish', '--registry', self.options.registry],
            stdin=p2.stdout,
            stdout=PIPE,
            cwd=self.cwd.as_posix()
        )
        p3.wait()

        p1.stdout.close()
        p2.stdout.close()
        p3.stdout.close()

        code = p3.returncode

        if code != 0:
            sys.stderr.write("PUBLISH ****      Can't upload JS package: " + self.cwd.as_posix() + "\n")
            self.print_last_npm_logs(50)
            sys.stderr.write("PUBLISH ****      Can't upload JS package: " + self.cwd.as_posix() + "\n")
            sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
            sys.exit(code)

        print("PUBLISH ****     Js package uploaded: " + self.cwd.as_posix())

import glob
import os
import sys
import json
import subprocess
from typing import List, Optional, Pattern, Match
from pathlib import Path
from subprocess import Popen, PIPE, check_output

from cmd.Tasks.PrintNpmLogs import PrintNpmLogs
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Publish(Task):
    NAME = Tasks.PUBLISH

    def __exec_for_json(self, args: List[str]) -> dict:
        ret = self.__exec_for_stdout(args)
        # print('RESULT `' + ret + '`')
        return json.loads(ret)

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, stderr=PIPE, cwd=self.cwd.as_posix()).communicate()
        stdout = self.__decode_stdout(stdout)
        # print('RESULT STDOUT `' + stdout + '`')
        stderr = self.__decode_stdout(stderr)
        print('RESULT STDERR`' + stderr + '`')
        return stdout if stdout != '' else stderr

    def __decode_stdout(self, stdout) -> str:
        return stdout.strip().decode('utf-8')

    def __should_unpublish(self) -> bool:
        print('****     ****    CHECK REGISTRY EXISTS')
        resp = self.__exec_for_json(
            ['npm', 'view', self.package.name(), '--registry', self.options.registry, '--json', '-s'])
        return resp.get('error') is None

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
        p_login = Popen(
            ['npm-cli-login', '-u', self.options.username, '-p', self.options.password, '-e', self.options.email, '-r',
             self.options.registry],
            stdout=PIPE,
            cwd=self.cwd.as_posix()
        )

        p_login.wait()
        code = p_login.returncode
        if code != 0:
            sys.stderr.write("LOGIN FAILED ****      Can't upload JS package: " + self.cwd.as_posix() + "\n")

            PrintNpmLogs.print_last_lines(50)

            sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
            sys.exit(code)
        print('****     ****    LOGGED')

        p_unpublish = None
        should_unpublish = self.__should_unpublish()

        if should_unpublish:
            print('****     ****    UNPUBLISH')

            if not self.package.version():
                sys.stderr.write(
                    "UNPUBLISH FAILED ****      Can't upload JS package: " + self.cwd.as_posix() + "\n" + "impossible to unpublish entire package, version is empty")
                sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
                sys.exit(code)

            p_unpublish = Popen(
                ['npm', 'unpublish', self.package.name() + '@' + self.package.version(), '--force', '--registry',
                 self.options.registry],
                stdin=p_login.stdout,
                stdout=PIPE,
                cwd=self.cwd.as_posix()
            )

            p_unpublish.wait()
            code = p_unpublish.returncode

            if code != 0:
                sys.stderr.write("UNPUBLISH FAILED ****      Can't upload JS package: " + self.cwd.as_posix() + "\n")

                PrintNpmLogs.print_last_lines(50)

                sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
                sys.exit(code)

            print('****     ****    UNPUBLISHED')
        else:
            print('****     ****    NEW PACKAGE')

        print('****     ****    PUBLISH')

        stdin = p_login.stdout
        if should_unpublish:
            stdin = p_unpublish.stdout

        p_publish = Popen(
            ['npm', 'publish', '--registry', self.options.registry],
            stdin=stdin,
            stdout=PIPE,
            cwd=self.cwd.as_posix()
        )
        p_publish.wait()

        p_login.stdout.close()
        if should_unpublish:
            p_unpublish.stdout.close()
        p_publish.stdout.close()

        code = p_publish.returncode

        if code != 0:
            sys.stderr.write("PUBLISH FAILED ****      Can't upload JS package: " + self.cwd.as_posix() + "\n")

            PrintNpmLogs.print_last_lines(50)

            sys.stderr.write("PUBLISH ****      Can't upload JS package: " + self.cwd.as_posix() + "\n")
            sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
            sys.exit(code)

        print("PUBLISH ****     Js package uploaded: " + self.cwd.as_posix())

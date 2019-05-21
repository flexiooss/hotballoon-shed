import sys
from subprocess import Popen, PIPE

from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks


class Publish(Task):
    NAME = Tasks.PUBLISH

    def process(self):
        print('PUBLISH : ' + self.package.name())

        if self.options.registry is None or self.options.email is None or self.options.password is None or self.options.username is None:
            raise ValueError('Publish need registry, username, password, email')

        print('****     registry : ' + self.options.registry)
        print('****     username : ' + self.options.username)
        print('****     email : ' + self.options.email)
        print('****     sources : ' + self.cwd.as_posix())

        print("deploying JS package in " + self.cwd.as_posix())

        p1 = Popen(
            ['npm-cli-login', '-u', self.options.username, '-p', self.options.password, '-e', self.options.email, '-r',
             self.options.registry],
            stdout=PIPE,
            cwd=self.cwd.as_posix()
        )

        p2 = Popen(
            ['npm' ,'publish', '--registry', self.options.registry, '-f'],
            stdin=p1.stdout,
            stdout=PIPE,
            cwd=self.cwd.as_posix()
        )

        p1.stdout.close()
        stdout, stderr = p2.communicate()
        p1.wait()
        p2.stdout.close()
        p2.wait()

        code = p2.returncode

        #         bash = Popen(["bash"], stdin=PIPE, stdout=PIPE, stderr=PIPE,
        #                      shell=True, cwd=self.cwd.as_posix())
        #
        #         commands = """\
        # npm-cli-login -u """ + self.options.username + """ -p """ + self.options.password + """ -e  """ + self.options.email + """ -r """ + self.options.registry + """ \
        # npm publish --registry """ + self.options.registry + """ -f \
        # exit 0
        # """
        #
        #         bash.stdin.write(commands)
        #         bash.stdin.flush()
        #         bash.wait()
        #         code = bash.returncode

        if code != 0:
            sys.stderr.write("Command terminated with wrong status code: " + str(code))
            sys.stderr.write("Can't upload JS package: " + self.cwd.as_posix())
            print("OUT: " + stdout.strip().decode('utf-8'))
            print("ERR: " + stderr.strip().decode('utf-8'))
            sys.exit(code)

        print("Js package uploaded: " + self.cwd.as_posix())

import getopt
import re
import sys
from pathlib import Path
from subprocess import Popen, PIPE

from typing import List, Optional

from cmd.Tasks.TaskBuilder import CaseBuilder
from cmd.Options import Options
from cmd.Tasks.Tasks import Tasks
from cmd.options.Resolver import Resolver


class Executor:
    tasks: Optional[List[Tasks]] = None
    options: Optional[Options] = None

    def __init__(self, cwd: Path) -> None:
        self.__cwd: Path = cwd
        self.__options_resolver: Resolver = Resolver()

    def __exec(self, args: List[str]) -> Popen:
        child: Popen = Popen(args, cwd=self.__cwd.as_posix())
        child.communicate()
        return child

    def __exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.__cwd.as_posix()).communicate()
        return self.__decode_stdout(stdout)

    def __decode_stdout(self, stdout) -> str:
        return stdout.strip().decode('utf-8')

    def extract_argv(self, argv: List[str]):
        self.__extract_options(argv)
        self.__extract_tasks(argv)

    def __extract_options(self, argv: List[str]):
        options: Options = Options()

        try:
            opts, args = getopt.gnu_getopt(
                argv,
                self.__options_resolver.short_name_options(),
                self.__options_resolver.name_options()
            )

        except getopt.GetoptError:
            print('OUPS !!!')
            print('Try `hshed -H`')
            sys.exit(2)

        for opt, arg in opts:
            arg = re.sub('[\s+]', '', arg)
            self.__options_resolver.resolve(opt=opt, arg=arg, options=options)
        self.options = options

    def __extract_tasks(self, argv: List[str]):
        tasks: List[Tasks] = []
        arg: str
        for arg in argv:
            arg = re.sub('[\s+]', '', arg).lower()
            if Tasks.has_value(arg):
                tasks.append(Tasks[arg.replace('-', '_').upper()])

        if len(tasks) == 0:
            raise ValueError('No tasks for this command')
        self.tasks = tasks

    def exec(self):
        case: CaseBuilder = CaseBuilder(self.tasks, self.options, self.__cwd)
        case.process()

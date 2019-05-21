import getopt
import re
import sys
from pathlib import Path

from typing import List, Optional

from cmd.Tasks.TaskBuilder import TaskBuilder
from cmd.Options import Options
from cmd.Tasks.Tasks import Tasks
from cmd.Tasks.TasksShortCut import TasksShortCut
from cmd.options.Resolver import Resolver


class Executor:
    tasks: Optional[List[Tasks]] = None
    options: Optional[Options] = None

    def __init__(self, cwd: Path) -> None:
        self.__cwd: Path = cwd
        self.__options_resolver: Resolver = Resolver()

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
            print('Oh buddy try `hbshed -H`')
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
            else:
                try:
                    if TasksShortCut[arg.replace('-', '_').upper()] is not None:
                        for task in TasksShortCut[arg.replace('-', '_').upper()].value.split():
                            tasks.append(Tasks[task.replace('-', '_').upper()])
                except KeyError:
                    pass

        if len(tasks) == 0:
            raise ValueError('No tasks for this command')
        self.tasks = tasks

    def exec(self):
        if self.options.source is not None:
            cwd: Path = Path(self.options.source)
            if not cwd.is_dir():
                raise FileNotFoundError('Bad source path given : ' + cwd.as_posix())
            self.__cwd = cwd

        taskbuilder: TaskBuilder = TaskBuilder(self.tasks, self.options, self.__cwd).process()

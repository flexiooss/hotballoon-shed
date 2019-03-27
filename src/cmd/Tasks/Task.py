from __future__ import annotations
import abc
from pathlib import Path
from subprocess import Popen, PIPE

from typing import List, Optional

from cmd.Options import Options
from cmd.Tasks import Tasks
from cmd.package.PackageHandler import PackageHandler


class Task(abc.ABC):
    NAME: Tasks

    def __init__(self, options: Options, package: Optional[PackageHandler], cwd: Path) -> None:
        self.options: Options = options
        self.package: Optional[PackageHandler] = package
        self.cwd: Path = cwd

    @abc.abstractmethod
    def process(self):
        pass

    def exec(self, args: List[str]) -> Popen:
        child: Popen = Popen(args, cwd=self.cwd.as_posix())
        child.communicate()
        return child

    def exec_for_stdout(self, args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE, cwd=self.cwd.as_posix()).communicate()
        return self.decode_stdout(stdout)

    def decode_stdout(self, stdout) -> str:
        return stdout.strip().decode('utf-8')

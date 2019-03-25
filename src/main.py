#! /usr/bin/env python3.7
import os
import re
import sys
from pathlib import Path
from subprocess import Popen
from typing import Optional, Dict, List

from cmd.Executor import Executor
from cmd.Subject import Subject


def main(argv) -> None:
    executor: Executor = Executor(cwd=Path.cwd())
    executor.extract_argv(argv)

    executor.exec()



    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])

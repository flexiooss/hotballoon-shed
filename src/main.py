#! /usr/bin/env python3.7
import sys
from pathlib import Path

from cmd.Executor import Executor


def main(argv) -> None:
    executor: Executor = Executor(cwd=Path.cwd())
    executor.extract_argv(argv)
    try:
        executor.exec()
    except:
        sys.exit(1)
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])

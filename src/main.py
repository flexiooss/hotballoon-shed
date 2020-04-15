#! /usr/bin/env python3.7
import sys
from pathlib import Path

from cmd.Executor import Executor


def main(argv) -> None:
    executor: Executor = Executor(cwd=Path.cwd())
    executor.extract_argv(argv)
    try:
        executor.exec()
    except (FileNotFoundError, FileExistsError, ImportError, AttributeError, ValueError, KeyError) as err:
        sys.stderr.write("""

\033[31m#######################################
# OUPS !!!
# {error}
#######################################\x1b[0m

""".format(error=err))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])

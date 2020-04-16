#! /usr/bin/env python3.7
import time

import sys
from pathlib import Path

from cmd.Executor import Executor


def main(argv) -> None:
    start_time: time = time.time()
    executor: Executor = Executor(cwd=Path.cwd())
    executor.extract_argv(argv)
    if executor.options.debug:
        executor.exec()
    else:
        try:
            executor.exec()
        except (FileNotFoundError, FileExistsError, ImportError, AttributeError, ValueError, KeyError) as err:
            sys.stderr.write("""
    
\033[31m#######################################
# OUPS !!!
# {type}:{error}
#######################################\x1b[0m
    
""".format(type=err.__class__.__name__, error=err))
            sys.stderr.write("Command terminated with wrong status code: 1" + "\n")
            sys.exit(1)
    if not executor.options.quiet:
        print("""
    
\033[32m#####################################################
# command terminated with success in %s seconds #
#####################################################\x1b[0m
""" % round((time.time() - start_time), 3))

    if executor.options.debug:
        sys.stderr.write("Command terminated with success status code: 0" + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])

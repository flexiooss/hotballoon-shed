from __future__ import annotations
import re
from typing import Dict, Match
from pathlib import Path
from subprocess import Popen
import os
from subprocess import Popen, PIPE


class Version:
    def __init__(self, string_version: str) -> None:
        self.string_version: str = string_version

    @staticmethod
    def exec(args: List[str]) -> Popen:
        child: Popen = Popen(args)
        child.communicate()
        return child

    @staticmethod
    def exec_for_stdout(args: List[str]) -> str:
        stdout, stderr = Popen(args, stdout=PIPE).communicate()
        return Version.decode_stdout(stdout)

    @staticmethod
    def decode_stdout(stdout) -> str:
        return stdout.strip().decode('utf-8')

    def satisfies(self, version: str) -> bool:
        # print('compare version : ' + self.string_version + '   ' + version)

        tester: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/semver.js')
        tester.resolve()

        if not tester.is_file():
            raise FileNotFoundError('No tester file found for this tester : ' + tester.as_posix())
        test_ret: str = Version.exec_for_stdout(
            ['node', tester.as_posix(), self.string_version, version])

        if test_ret == 'true':
            return True
        if test_ret == 'false':
            return False

        raise ValueError('can not compare version : ' + self.string_version + '   ' + version)

import os
import sys
from cmd.options.Option import Option


class HelpOption(Option):
    HAS_VALUE = False
    SHORT_NAME = 'H'
    NAME = 'help'

    def exec(self):
        file = open(os.path.dirname(os.path.abspath(__file__)) + '/../../help.txt', 'r')
        print(file.read())
        sys.exit()

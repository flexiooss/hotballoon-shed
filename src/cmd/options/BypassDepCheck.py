from cmd.Options import Options
from cmd.options.Option import Option


class BypassDepCheck(Option):
    HAS_VALUE = False
    SHORT_NAME = 'X'
    NAME = 'bypass_dep_check'

    def exec(self) -> Options:
        self.options.bypass_dep_check = True
        return self.options

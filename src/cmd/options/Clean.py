from cmd.Options import Options
from cmd.options.Option import Option


class Clean(Option):
    HAS_VALUE = False
    SHORT_NAME = 'C'
    NAME = 'clean'

    def exec(self) -> Options:
        self.options.clean = self.arg
        return self.options

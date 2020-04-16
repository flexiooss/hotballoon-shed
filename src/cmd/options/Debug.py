from cmd.Options import Options
from cmd.options.Option import Option


class Debug(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'debug'

    def exec(self) -> Options:
        self.options.debug = True
        return self.options

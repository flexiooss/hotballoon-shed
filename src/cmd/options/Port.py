from cmd.Options import Options
from cmd.options.Option import Option


class Port(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'port'

    def exec(self) -> Options:
        self.options.port = self.arg
        return self.options

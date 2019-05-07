from cmd.Options import Options
from cmd.options.Option import Option


class Source(Option):
    HAS_VALUE = True
    SHORT_NAME = 'S'
    NAME = 'source'

    def exec(self) -> Options:
        self.options.source = self.arg
        return self.options

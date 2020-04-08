from cmd.Options import Options
from cmd.options.Option import Option


class Entry(Option):
    HAS_VALUE = True
    SHORT_NAME = 'E'
    NAME = 'entry'

    def exec(self) -> Options:
        self.options.entry = self.arg
        return self.options

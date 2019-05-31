from cmd.Options import Options
from cmd.options.Option import Option


class Restrict(Option):
    HAS_VALUE = True
    SHORT_NAME = 'R'
    NAME = 'restrict'

    def exec(self) -> Options:
        self.options.restrict = self.arg
        return self.options

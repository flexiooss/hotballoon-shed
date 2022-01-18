from cmd.Options import Options
from cmd.options.Option import Option


class Strict(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'strict'

    def exec(self) -> Options:
        self.options.strict = True
        return self.options

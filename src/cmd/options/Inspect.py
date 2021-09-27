from cmd.Options import Options
from cmd.options.Option import Option


class Inspect(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'inspect'

    def exec(self) -> Options:
        self.options.inspect = True
        return self.options

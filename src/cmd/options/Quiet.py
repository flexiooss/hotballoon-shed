from cmd.Options import Options
from cmd.options.Option import Option


class Quiet(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'quiet'

    def exec(self) -> Options:
        self.options.quiet = True
        return self.options

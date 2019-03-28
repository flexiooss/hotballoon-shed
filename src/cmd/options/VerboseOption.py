from cmd.Options import Options
from cmd.options.Option import Option


class VerboseOption(Option):
    HAS_VALUE = False
    SHORT_NAME = 'V'
    NAME = 'verbose'

    def exec(self) -> Options:
        self.options.verbose = True
        return self.options

from cmd.Options import Options
from cmd.options.Option import Option


class Bundle(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'bundle'

    def exec(self) -> Options:
        self.options.bundle = True
        print('[DEPRECATED: bundle option is now deprecated prefer output-type build option]')
        return self.options

from cmd.Options import Options
from cmd.options.Option import Option


class Registry(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'registry'

    def exec(self) -> Options:
        self.options.registry = self.arg
        return self.options

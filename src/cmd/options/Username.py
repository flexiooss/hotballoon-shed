from cmd.Options import Options
from cmd.options.Option import Option


class Username(Option):
    HAS_VALUE = True
    SHORT_NAME = 'U'
    NAME = 'username'

    def exec(self) -> Options:
        self.options.username = self.arg
        return self.options

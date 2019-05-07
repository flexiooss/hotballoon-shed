from cmd.Options import Options
from cmd.options.Option import Option


class Password(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'password'

    def exec(self) -> Options:
        self.options.password = self.arg
        return self.options

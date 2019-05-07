from cmd.Options import Options
from cmd.options.Option import Option


class Email(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'email'

    def exec(self) -> Options:
        self.options.email = self.arg
        return self.options

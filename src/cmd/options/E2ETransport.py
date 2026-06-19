from cmd.Options import Options
from cmd.options.Option import Option


class E2ETransport(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'e2e-transport'

    def exec(self) -> Options:
        self.options.e2e_transport = self.arg
        return self.options

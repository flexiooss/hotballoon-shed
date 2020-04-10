from cmd.Options import Options
from cmd.options.Option import Option


class ServerConfig(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'server-config'

    def exec(self) -> Options:
        self.options.server_config = self.arg
        return self.options

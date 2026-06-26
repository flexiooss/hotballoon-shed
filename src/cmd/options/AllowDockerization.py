from cmd.Options import Options
from cmd.options.Option import Option


class AllowDockerization(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'allow-dockerization'

    def exec(self) -> Options:
        self.options.allow_dockerization = True
        return self.options

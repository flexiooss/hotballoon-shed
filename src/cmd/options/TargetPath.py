from cmd.Options import Options
from cmd.options.Option import Option


class TargetPath(Option):
    HAS_VALUE = True
    SHORT_NAME = 'T'
    NAME = 'target'

    def exec(self) -> Options:
        self.options.target_path = self.arg
        return self.options

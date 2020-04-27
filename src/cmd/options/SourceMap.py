from cmd.Options import Options
from cmd.options.Option import Option


class SourceMap(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'source-map'

    def exec(self) -> Options:
        self.options.source_map = True
        return self.options

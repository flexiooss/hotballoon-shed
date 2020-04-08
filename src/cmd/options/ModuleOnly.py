from cmd.Options import Options
from cmd.options.Option import Option


class ModuleOnly(Option):
    HAS_VALUE = False
    SHORT_NAME = None
    NAME = 'module-only'

    def exec(self) -> Options:
        self.options.module_only = True
        return self.options

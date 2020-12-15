from cmd.Options import Options
from cmd.options.Option import Option


class HTMLTemplate(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'html-template'

    def exec(self) -> Options:
        self.options.html_template = self.arg
        return self.options

from cmd.Options import Options
from cmd.options.Option import Option


class HTMLTemplateName(Option):
    HAS_VALUE = True
    SHORT_NAME = None
    NAME = 'html-template-name'

    def exec(self) -> Options:
        self.options.html_template_name = self.arg
        return self.options

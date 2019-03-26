from typing import List

from cmd.Options import Options
from cmd.options.HelpOption import HelpOption
from cmd.options.Option import Option
from cmd.options.VerboseOption import VerboseOption


class Resolver:
    options: List[Option] = [VerboseOption, HelpOption]

    def resolve(self, opt: str, arg: str, options: Options):
        o: Option
        for o in self.options:
            o.process(opt=opt, arg=arg, options=options)

    def short_name_options(self) -> str:
        ret: str = ''
        for o in self.options:
            ret += o.SHORT_NAME
            if (o.HAS_VALUE == True):
                ret += ':'
        return ret

    def name_options(self) -> List[str]:
        ret: List[str] = []
        for o in self.options:
            v: str = o.NAME
            if (o.HAS_VALUE == True):
                v += '='
        ret.append(v)
        return ret

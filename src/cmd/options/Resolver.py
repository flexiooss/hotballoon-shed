from typing import List

from cmd.Options import Options
from cmd.options.Email import Email
from cmd.options.Password import Password
from cmd.options.Registry import Registry
from cmd.options.Restrict import Restrict
from cmd.options.Source import Source
from cmd.options.Username import Username
from cmd.options.HelpOption import HelpOption
from cmd.options.Option import Option
from cmd.options.VerboseOption import VerboseOption
from cmd.options.TargetPath import TargetPath
from cmd.options.Clean import Clean
from cmd.options.ModuleOnly import ModuleOnly


class Resolver:
    options: List[Option] = [Source, VerboseOption, HelpOption, TargetPath, Username, Password, Email, Registry,
                             Restrict, Clean, ModuleOnly]

    def resolve(self, opt: str, arg: str, options: Options):
        o: Option
        for o in self.options:
            o.process(opt=opt, arg=arg, options=options)

    def short_name_options(self) -> str:
        ret: str = ''
        for o in self.options:
            if o.SHORT_NAME is not None:
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

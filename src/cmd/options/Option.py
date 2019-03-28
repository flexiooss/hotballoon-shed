from __future__ import annotations
import abc

from cmd.Options import Options


class Option(abc.ABC):
    arg: str = None
    opt: str = None
    HAS_VALUE: bool
    SHORT_NAME: str
    NAME: str

    def __init__(self, opt: str, arg: str, options: Options) -> None:
        self.opt: str = opt
        self.arg: str = arg
        self.options: Options = options

    def test(self) -> bool:
        return self.opt in ('-' + self.SHORT_NAME, '--' + self.NAME)

    @abc.abstractmethod
    def exec(self) -> Options:
        pass

    @classmethod
    def process(cls, opt: str, arg: str, options: Options):
        option: Option = cls(opt, arg, options)
        if option.test():
            option.exec()

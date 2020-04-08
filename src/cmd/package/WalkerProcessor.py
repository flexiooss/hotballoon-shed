from __future__ import annotations
import abc

from cmd.package.PackageHandler import PackageHandler


class WalkerProcessor(abc.ABC):

    @abc.abstractmethod
    def process(self, package: PackageHandler):
        pass

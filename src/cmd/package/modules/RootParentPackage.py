from typing import Optional
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from pathlib import Path


class RootParentPackage:
    @staticmethod
    def from_module_package(package: HBShedPackageHandler) -> HBShedPackageHandler:
        if not package.config().has_parent():
            return package

        else:
            current_path: Path = package.cwd
            parent_package: HBShedPackageHandler = package

            while parent_package.config().has_parent() and not parent_package.config().is_parent_external():
                current_path = parent_package.cwd.parent
                parent_package = HBShedPackageHandler(current_path)

            return parent_package

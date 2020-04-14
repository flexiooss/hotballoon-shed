from cmd.package.AbstractDependenciesWalker import AbstractDependenciesWalker
from cmd.package.PackageHandler import PackageHandler


class DevDependenciesWalker(AbstractDependenciesWalker):

    def process_all(self):

        package: PackageHandler = self.process()
        if package.has_dev_dependencies():

            name: str
            version: str
            for name, version in package.dev_dependencies().items():
                DevDependenciesWalker(
                    target_package_name=name,
                    node_modules=self.node_modules,
                    processors=self.processors
                ).process_all()

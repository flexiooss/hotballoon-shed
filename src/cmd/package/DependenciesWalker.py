from cmd.package.AbstractDependenciesWalker import AbstractDependenciesWalker
from cmd.package.PackageHandler import PackageHandler


class DependenciesWalker(AbstractDependenciesWalker):

    def process_all(self):
        package: PackageHandler = self.process()

        if package.has_dependencies():

            name: str
            version: str
            for name, version in package.dependencies().items():

                DependenciesWalker(
                    target_package_name=name,
                    target_package_version=version,
                    node_modules=self.node_modules,
                    processors=self.processors,
                    prev_package=package
                ).process_all()

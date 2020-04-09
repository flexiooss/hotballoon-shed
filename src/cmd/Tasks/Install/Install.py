from pathlib import Path
from typing import Optional

from cmd.Options import Options
from cmd.Tasks.PrintNpmLogs import PrintNpmLogs
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler
from cmd.package.modules.RootParentPackage import RootParentPackage
from subprocess import Popen, PIPE
from cmd.Tasks.Install.CheckModuleDependencies import CheckModuleDependencies
from cmd.Tasks.Clean.CleanDependenciesDir import CleanDependenciesDir
from cmd.Tasks.Install.ModulePeerDependenciesProvisioner import ModulePeerDependenciesProvisioner
from cmd.Tasks.Install.ApplyModulePeerDependencies import ApplyModulePeerDependencies
import sys


class Install(Task):
    NAME = Tasks.INSTALL

    def __init__(self, options: Options, package: Optional[HBShedPackageHandler], cwd: Path,
                 node_modules: Optional[Path] = None) -> None:
        super().__init__(options, package, cwd)
        self.__node_modules: Optional[Path] = node_modules if node_modules is not None else cwd
        self.__ensure_node_modules()

    def __ensure_node_modules(self):
        if self.__node_modules is None:
            self.__node_modules = self.cwd

    def __modules_install(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                Install(self.options, module.package, module.package.cwd, self.__node_modules).process()

    def __check_modules_dependencies(self):
        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                CheckModuleDependencies(
                    root_package=self.package,
                    module=module
                ).process()

    def __check_root_parent(self):
        if self.package.config().has_parent():
            if self.package.dependencies().get(
                    self.package.config().parent_name()) != self.package.config().parent_version():
                raise FileNotFoundError(
                    'Root package parent have a parent not found or on bad version : ' + self.package.config().parent_name() + ':' + self.package.config().parent_version())

    def __provision_modules_peer_dependencies(self):
        provisioner: ModulePeerDependenciesProvisioner = ModulePeerDependenciesProvisioner(
            package=self.package
        )
        provisioner.prepare()
        print('#### peerDependencies found : ' + str(provisioner.count()))
        print('#### peerDependencies set to package')

        provisioner.apply(self.package)

        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                ApplyModulePeerDependencies(
                    root_package=self.package,
                    module=module,
                    provisioner=provisioner
                ).process()

            print('#### peerDependencies set to Modules')

    def __install(self):

        print('#### INSTALL : ' + self.package.name())

        self.__check_root_parent()

        if self.options.registry is None or self.options.email is None or self.options.password is None or self.options.username is None:

            self.exec(['npm', 'install', '--prefix', self.__node_modules.as_posix(), '--no-package-lock', '--force'])

            print('## INSTALL node_modules at : ' + self.__node_modules.as_posix())

        else:

            print('****     registry : ' + self.options.registry)
            print('****     username : ' + self.options.username)
            print('****     email : ' + self.options.email)
            print('****     ****    LOGIN')

            p1 = Popen(
                ['npm-cli-login', '-u', self.options.username, '-p', self.options.password, '-e', self.options.email,
                 '-r',
                 self.options.registry],
                stdout=PIPE,
                cwd=self.cwd.as_posix()
            )

            p1.wait()
            code = p1.returncode

            if code != 0:
                sys.stderr.write("LOGIN ****      Can't login to " + self.options.registry + "\n")

                PrintNpmLogs.print_last_lines(50)

                sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
                sys.exit(code)

            print('****     ****    LOGGED')

            print('## INSTALL node_modules at : ' + self.__node_modules.as_posix())

            p2 = Popen(
                ['npm', 'install', '--prefix', self.__node_modules.as_posix(), '--no-package-lock', '--force'],
                stdin=p1.stdout,
                stdout=PIPE,
                cwd=self.cwd.as_posix()
            )

            p2.wait()
            p1.stdout.close()
            p2.stdout.close()

            code = p2.returncode

            if code != 0:
                sys.stderr.write("INSTALL ****      Can't install at" + self.__node_modules.as_posix() + "\n")

                sys.stderr.write("Command terminated with wrong status code: " + str(code) + "\n")
                sys.exit(code)

            print('****     ****    INSTALL COMPLETE')
            PrintNpmLogs.print_last_lines(50)

    def __install_from_root_parent(self):
        root_parent_package: HBShedPackageHandler = RootParentPackage.from_module_package(self.package)
        print('#### root package parent found : ' + root_parent_package.name())

        CleanDependenciesDir(self.options, root_parent_package, root_parent_package.cwd).process()

        return Install(
            options=self.options,
            package=root_parent_package,
            cwd=root_parent_package.cwd,
            node_modules=None
        ).process()

    def process(self):
        if self.package.config().has_parent() and not self.package.config().has_parent_version():
            print('#### INSTALL from module : ' + self.package.name())
            self.__install_from_root_parent()
        else:
            self.__install()
            self.__check_modules_dependencies()
            self.__provision_modules_peer_dependencies()

import time
from pathlib import Path
from typing import Optional, Set, Dict

from cmd.Options import Options
from cmd.Tasks.Install.CheckParentDependencies import CheckParentDependencies
from cmd.Tasks.Install.CheckParents import CheckParents
from cmd.Tasks.Install.DependenciesProvisioner import DependenciesProvisioner
from cmd.Tasks.Install.ExternalModulesDependenciesProcessor import ExternalModulesDependenciesProcessor
from cmd.Tasks.Install.AncestorDependenciesCheck import AncestorDependenciesCheck
from cmd.Tasks.Install.ParentDependenciesWalkerProcessor import ParentDependenciesWalkerProcessor
from cmd.Tasks.Install.ParentWalkerProcessor import ParentWalkerProcessor
from cmd.Tasks.Install.PeerDependenciesWalkerProcessor import PeerDependenciesWalkerProcessor
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
from cmd.Tasks.Install.ApplyModulePeerDependencies import ApplyModulePeerDependencies
import sys


class Install(Task):
    NAME = Tasks.INSTALL
    __peer_processor: PeerDependenciesWalkerProcessor
    __parent_processor: ParentWalkerProcessor
    __parent_dependencies_processor: ParentDependenciesWalkerProcessor
    __external_modules_dependencies_processor: ExternalModulesDependenciesProcessor

    def __init__(self, options: Options, package: Optional[HBShedPackageHandler], cwd: Path,
                 node_modules: Optional[Path] = None) -> None:
        super().__init__(options, package, cwd)
        self.__node_modules: Optional[Path] = node_modules if node_modules is not None else cwd
        self.__ensure_node_modules()

    def __ensure_node_modules(self):
        if self.__node_modules is None:
            self.__node_modules = self.cwd

    def __ensure_processors(self):
        sys.stdout.write('#### prepare dependencies check  ')
        sys.stdout.flush()
        self.__peer_processor = PeerDependenciesWalkerProcessor()
        self.__parent_processor = ParentWalkerProcessor()
        self.__parent_dependencies_processor = ParentDependenciesWalkerProcessor()
        self.__external_modules_dependencies_processor = ExternalModulesDependenciesProcessor()

        DependenciesProvisioner(
            package=self.package,
            peer_processor=self.__peer_processor,
            parent_processor=self.__parent_processor,
            parent_dependencies_processor=self.__parent_dependencies_processor
        ).process()
        sys.stdout.write("\n")

    def __check_modules_dependencies(self):
        print('#### CHECK MODULES DEPENDENCIES & DEV_DEPENDENCIES')

        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                CheckModuleDependencies(
                    root_package=self.package,
                    parent_package=self.package,
                    module=module,
                    processor=self.__external_modules_dependencies_processor
                ).process()

    def __check_root_package_parent_dependencies(self):
        external_root_dependencies: Set[str] = self.__external_modules_dependencies_processor.dependencies

        if self.package.config().has_dependencies():
            external_root_dependencies = external_root_dependencies.union(self.package.config().dependencies())

        if len(external_root_dependencies):
            print('#### external dependencies into ancestors to check found : ' + str(len(external_root_dependencies)))

            sys.stdout.write('#### #### check ancestors dependencies ')
            sys.stdout.flush()

            AncestorDependenciesCheck(
                root_package=self.package,
                package=self.package,
                dependencies=external_root_dependencies
            ).process()

            sys.stdout.write("\n")

            if len(external_root_dependencies):
                raise FileNotFoundError(
                    'These dependencies are not declared by any parents : ' + "\n" + "\n   -  ".join(
                        external_root_dependencies))

    def __check_external_parent(self):

        print('#### parents to check found : ' + str(self.__parent_processor.count()))

        if self.__parent_processor.count():
            sys.stdout.write('#### #### check parents ')
            sys.stdout.flush()

            CheckParents(
                root_package=self.package,
                parents=self.__parent_processor.parents
            ).process()

            sys.stdout.write("\n")

    def __provision_modules_peer_dependencies(self):

        print('#### peerDependencies found : ' + str(self.__peer_processor.count()))
        dependencies: Dict[str, str] = {}
        for key in sorted(self.__peer_processor.dependencies.keys()):
            dependencies[key] = self.__peer_processor.dependencies[key]

        ApplyModulePeerDependencies(
            package=self.package,
            dependencies=dependencies
        ).process()

        print('#### #### peerDependencies set to parent & modules')

    def __check_external_parent_dependencies(self):
        print('#### all parents dependencies to presence check found : ' + str(
            self.__parent_dependencies_processor.count()))

        if self.__parent_dependencies_processor.count():
            sys.stdout.write('#### #### check parents dependencies ')
            sys.stdout.flush()

            CheckParentDependencies(
                root_package=self.package,
                dependencies=self.__parent_dependencies_processor.dependencies
            ).process()
            sys.stdout.write("\n")

    def __install(self):
        print('#### INSTALL : ' + self.package.name())

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

    def __message(self):
        if not self.options.quiet:
            print("""##############################################################################
 _           _   _           _ _                             _              _
| |         | | | |         | | |                           | |            | |
| |__   ___ | |_| |__   __ _| | | ___   ___  _ __ ______ ___| |__   ___  __| |
| '_ \ / _ \| __| '_ \ / _` | | |/ _ \ / _ \| '_ \______/ __| '_ \ / _ \/ _` |
| | | | (_) | |_| |_) | (_| | | | (_) | (_) | | | |     \__ \ | | |  __/ (_| |
|_| |_|\___/ \__|_.__/ \__,_|_|_|\___/ \___/|_| |_|     |___/_| |_|\___|\__,_|

https://github.com/flexiooss/hotballoon-shed
###############################################################################
              """)

    def process(self):
        if self.package.config().has_parent() and not self.package.config().is_parent_external():
            print('#### INSTALL from module : ' + self.package.name())
            self.__install_from_root_parent()
        else:
            self.__install()
            self.__message()
            self.__ensure_processors()
            self.__check_modules_dependencies()
            self.__check_root_package_parent_dependencies()
            self.__check_external_parent()
            self.__check_external_parent_dependencies()
            self.__provision_modules_peer_dependencies()

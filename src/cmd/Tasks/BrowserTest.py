import os
import shlex
import sys
import time
from pathlib import Path
from subprocess import Popen
from typing import Optional

from cmd.Options import Options
from cmd.Tasks.Task import Task
from cmd.Tasks.Tasks import Tasks
from cmd.package.HBShedPackageHandler import HBShedPackageHandler
from cmd.package.modules.Module import Module
from cmd.package.modules.ModulesHandler import ModulesHandler
from cmd.package.modules.RootParentPackage import RootParentPackage

BROWSER_TESTS_DIR = '/tmp/hotballoon-shed/browser-tests'


# Note: really only supports playwright at every level
class BrowserTest(Task):
    NAME = Tasks.BROWSER_TEST

    def __init__(self, options: Options, package: Optional[HBShedPackageHandler], cwd: Path):
        super().__init__(options, package, cwd)
        self.__reminder = None

    def __ensure_folders(self, run_dir: str, transport: str):
        Path(os.path.join(run_dir, 'dist')).mkdir(0o700, parents=True, exist_ok=True)
        Path(os.path.join(run_dir, 'tests')).mkdir(0o700, parents=True, exist_ok=True)

    def __build_modules(self, run_dir: str):
        if self.package is None: return

        if self.package.config().has_browser_test():
            self.__build_module(run_dir)

        if self.package.config().has_modules():
            modules: ModulesHandler = ModulesHandler(self.package)
            module: Module
            for module in modules.modules:
                BrowserTest(self.options, module.package, module.package.cwd).__build_modules(run_dir)

    def __build_module(self, run_dir: str):
        if self.package is None: return
        if not self.package.config().browser_has_test_dir(): return

        module_name = self.package.name()
        dist_dir = os.path.join(run_dir, 'dist', module_name)
        tests_link = os.path.join(run_dir, 'tests', module_name)

        if os.path.exists(dist_dir) or os.path.lexists(tests_link):
            raise ValueError('Duplicate browser-test module name: ' + module_name)

        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

        print('**** BUILD MODULE: ' + module_name)

        builder: Path = Path(os.path.dirname(
            os.path.realpath(
                __file__)) + '/../../build/' + self.package.config().builder() + '/production_debug.js').resolve()
        if not builder.is_file():
            raise FileNotFoundError('No builder file found for this builder : ' + self.package.config().builder())

        verbose: str = '-v' if self.options.verbose else ''

        html_template: Path = Path(
            os.path.dirname(os.path.realpath(__file__)) + '/../../build/html/minimal/index.html').resolve()
        if not html_template.is_file():
            raise FileNotFoundError('Could not find HTML template')

        test_dir = self.package.config().browser_test_dir()
        if not test_dir.is_dir():
            raise FileNotFoundError('Could not find test dir: ' + test_dir.as_posix())
        print('**** TESTS DIR: ' + test_dir.as_posix(), flush=True)

        child: Popen = self.exec([
            'node',
            builder.as_posix(),
            verbose,
            '{"main": {"import": "' + test_dir.as_posix() + '/browser-fixture.js"}}',
            html_template.as_posix(),
            dist_dir
        ])
        code = child.returncode

        if code != 0:
            sys.stderr.write("BUILD APP DEBUG FAIL" + "\n")
            raise ChildProcessError(code)

        os.symlink(
            test_dir.as_posix(),
            tests_link,
            True
        )

    def __run_tests(self, run_dir: str, transport: str):
        if self.package is None: return

        browser_tester = self.package.config().browser_tester()
        tester: Path = Path(os.path.dirname(
            os.path.realpath(__file__)) + '/../../browser-tests/' + browser_tester + '/playwright.config.js').resolve()
        if not tester.is_file():
            raise FileNotFoundError('No tester file found for this tester: ' + browser_tester)

        os.environ['E2E_RUN_DIR'] = run_dir

        print('**** INVOKING TESTER', flush=True)
        match browser_tester:
            case 'playwright':
                args = [
                    'npx',
                    'playwright',
                    'test',
                    '--config', tester.as_posix()
                ]
                if transport == 'dev':
                    args.append('--ui')

                child = self.exec(args)

                print('\n**** Tests completed')
                if self.__reminder is not None: print('**** reminder: ' + self.__reminder)

                match transport:
                    case 'static' | 'dev':
                        print('**** Additional assets may be available in the `test-results` folder')
                    case 'docker':
                        print('**** Assets can be found in the the container\'s `/test-results` folder')
                        print('**** If it was mounted as a shared volume, you can find them on your mount point')
                        print('**** To see the full report: `npx playwright show-report <mount-point>/playwright/html`')

                        code = child.returncode
                        if code != 0:
                            sys.stderr.write('**** ERROR RETURNED BY PLAYWRIGHT\n')
                            raise ChildProcessError(code)
            case _:
                raise ValueError('Unsupported browser tester: ' + browser_tester)

    def __run_in_docker_and_exit(self):
        if self.package is None: return
        print('**** It seems that you are not running this from the ci-js-tools image!')
        package_path = RootParentPackage.from_module_package(self.package).cwd.as_posix()

        command = [
            'docker', 'run', '--rm', '--ipc=host',
            '--user', str(os.getuid()),
            '-v', package_path + ':/src',
            '-v', '/tmp/test-results:/test-results',
            '--workdir', '/src/' + os.path.relpath(Path.cwd().as_posix(), package_path),
            'codingmatters/ci-js-tools',
            'hbshed', 'browser-test', '--e2e-transport=docker'
        ]

        print(
            'Here is the suggested command for using docker. We will ensure the `/tmp/test-results` folder exists.')
        print('Press enter to accept and run.')
        input(shlex.join(command))

        Path('/tmp/test-results').mkdir(0o700, parents=True, exist_ok=True)
        code = self.exec(command).returncode
        print('**** docker invocation completed')
        sys.exit(code)

    def __check_js_tools(self, transport: str, is_tools: bool):
        if self.package is None: return
        if is_tools:
            match transport:
                case 'dev':
                    raise EnvironmentError('dev transport is meant to be used without docker')
                case 'static':
                    raise EnvironmentError(
                        'static transport is meant to be used without docker. Use `--e2e-transport=docker` if you want standardized visual tests')
                case 'docker':
                    print('**** DOCKER TRANSPORT MODE')
                    self.__reminder = 'don\'t forget to check and commit any generated screenshots'
        else:
            match transport:
                case 'dev':
                    print('**** DEV TRANSPORT MODE')
                    self.__reminder = 'generated screenshots using this mode are NOT standardized and must NOT be committed'
                case 'static':
                    print('**** STATIC TRANSPORT MODE')
                    self.__reminder = 'This mode ignores visual tests. Use the docker transport mode if needed'
                case 'docker':
                    print('**** DOCKER TRANSPORT MODE')
                    self.__run_in_docker_and_exit()
        if self.__reminder is not None: print('**** note: ' + self.__reminder)

    def __ensure_builder(self):
        if not self.package.config().has_builder():
            raise KeyError('No builder found into `hotballoon-shed` configuration')

    def process(self):
        if self.package is None: return
        self.__reminder = None

        print('BROWSER TEST: ' + self.package.name())
        if not self.package.config().has_browser_tester():
            raise KeyError(
                'No browser tester found for this package. If you want to run tests in sub-modules, you must at least add a tester entry in this module, without path.')

        run_dir = os.path.join(BROWSER_TESTS_DIR, str(time.time_ns()))

        transport = self.options.e2e_transport or 'static'
        os.environ['E2E_TRANSPORT'] = transport
        if self.options.verbose:
            os.environ['E2E_VERBOSE'] = '1'

        self.__check_js_tools(transport, os.environ.__contains__('CI_JS_TOOLS'))

        self.__ensure_folders(run_dir, transport)

        match transport:
            case 'dev':
                # Reuses `hbshed dev`
                if not self.package.config().browser_has_test_dir():
                    raise KeyError('No browser test dir found for this package')
                os.environ['E2E_TEST_DIR'] = (self.cwd / self.package.config().browser_test_dir()).as_posix()

            case 'static' | 'docker':
                print('**** BUILD FIXTURES')
                self.__ensure_builder()
                self.__build_modules(run_dir)

            case _:
                raise ValueError('Unknown E2E transport mode: ' + transport)

        self.__run_tests(run_dir, transport)

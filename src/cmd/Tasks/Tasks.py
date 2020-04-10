from enum import Enum, unique


@unique
class Tasks(Enum):
    BUILD: str = 'build'
    CLEAN: str = 'clean'
    CLEAN_DEPENDENCIES_DIR: str = 'clean-dependencies-dir'
    CLEAN_BUILD: str = 'clean-build'
    CLEAN_SOURCES: str = 'clean-sources'
    CLEAN_TESTS: str = 'clean-tests'
    CLEAN_PEER_DEPENDENCIES: str = 'clean-peerDependencies'
    DEV: str = 'dev'
    EXTRACT_PACKAGE: str = 'extract-package'
    INSTALL: str = 'install'
    GENERATE_SOURCES: str = 'generate-sources'
    PUBLISH: str = 'publish'
    SELF_INSTALL: str = 'self-install'
    SET_FLEXIO_REGISTRY: str = 'set-flexio-registry'
    TEST: str = 'test'
    BROWSER_TEST: str = 'browser-test'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))

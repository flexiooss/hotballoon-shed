from enum import Enum, unique


@unique
class Tasks(Enum):
    BUILD: str = 'build'
    CLEAN: str = 'clean'
    DEV: str = 'dev'
    INSTALL: str = 'install'
    GENERATE_SOURCES: str = 'generate-sources'
    TEST: str = 'test'
    SELF_INSTALL: str = 'self-install'
    SET_FLEXIO_REGISTRY: str = 'set-flexio-registry'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))

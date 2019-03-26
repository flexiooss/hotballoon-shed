from enum import Enum, unique


@unique
class Tasks(Enum):
    BUILD: str = 'build'
    CLEAN: str = 'clean'
    DEV: str = 'dev'
    INSTALL: str = 'install'
    GENERATE: str = 'generate'
    TEST: str = 'test'
    SELF_INSTALL:str = 'self-install'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))

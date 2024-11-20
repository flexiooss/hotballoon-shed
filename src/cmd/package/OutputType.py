from enum import Enum, unique


@unique
class OutputType(Enum):
    PRODUCTION: str = 'production'
    DEBUG: str = 'debug'
    BUNDLE: str = 'bundle'

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))

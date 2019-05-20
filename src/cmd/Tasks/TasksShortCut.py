from enum import Enum, unique

from cmd.Tasks.Tasks import Tasks


@unique
class TasksShortCut(Enum):
    CIG: str = Tasks.CLEAN.value + ' ' + Tasks.INSTALL.value + ' ' + Tasks.GENERATE_SOURCES.value

    @classmethod
    def has_value(cls, value) -> bool:
        return bool(any(value == item.value for item in cls))

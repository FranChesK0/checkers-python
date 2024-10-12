import enum


class CheckerType(enum.Enum):
    NONE: int = enum.auto()
    WHITE_MAN: int = enum.auto()
    BLACK_MAN: int = enum.auto()
    WHITE_KING: int = enum.auto()
    BLACK_KING: int = enum.auto()


class Checker:
    def __init__(self, type: CheckerType = CheckerType.NONE) -> None:
        self.__type = type

    @property
    def type(self) -> CheckerType:
        return self.__type

    @type.setter
    def type(self, type: CheckerType) -> None:
        self.__type = type

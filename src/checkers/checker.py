from .enums import CheckerType


class Checker:
    def __init__(self, type: CheckerType) -> None:
        self.__type = type

    @property
    def type(self) -> CheckerType:
        return self.__type

    def change_type(self, type: CheckerType) -> None:
        self.__type = type

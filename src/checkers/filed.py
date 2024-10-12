from functools import reduce

from .checker import Checker, CheckerType
from .constants import BLACK_CHECKERS, WHITE_CHECKERS


class Field:
    def __init__(self, x_size: int, y_size: int) -> None:
        self.__x_size = x_size
        self.__y_size = y_size
        self.__generate()

    @property
    def x_size(self) -> int:
        return self.__x_size

    @property
    def y_size(self) -> int:
        return self.__y_size

    @property
    def size(self) -> int:
        return max(self.x_size, self.y_size)

    @property
    def white_checkers_count(self) -> int:
        return sum(
            reduce(
                lambda acc, checker: acc + (checker.type in WHITE_CHECKERS), checkers, 0
            )
            for checkers in self.__checkers
        )

    @property
    def black_checkers_count(self) -> int:
        return sum(
            reduce(
                lambda acc, checker: acc + (checker.type in BLACK_CHECKERS), checkers, 0
            )
            for checkers in self.__checkers
        )

    @property
    def white_score(self) -> int:
        return sum(
            reduce(
                lambda acc, checker: acc
                + (checker.type == CheckerType.WHITE_MAN)
                + (checker.type == CheckerType.WHITE_KING) * 3,
                checkers,
                0,
            )
            for checkers in self.__checkers
        )

    @property
    def black_score(self) -> int:
        return sum(
            reduce(
                lambda acc, checker: acc
                + (checker.type == CheckerType.BLACK_KING)
                + (checker.type == CheckerType.BLACK_KING) * 3,
                checkers,
                0,
            )
            for checkers in self.__checkers
        )

    @classmethod
    def copy(cls, field: "Field") -> "Field":
        field_copy = cls(field.x_size, field.y_size)

        for y in range(field.y_size):
            for x in range(field.x_size):
                field_copy.at(x, y).type = field.type_at(x, y)

        return field_copy

    def __generate(self) -> None:
        self.__checkers = [
            [Checker() for _ in range(self.x_size)] for _ in range(self.y_size)
        ]

        for y in range(self.y_size):
            for x in range(self.x_size):
                if (y + x) % 2:
                    if y < 3:
                        self.__checkers[y][x].type = CheckerType.BLACK_MAN
                    elif y >= self.y_size - 3:
                        self.__checkers[y][x].type = CheckerType.WHITE_MAN

    def type_at(self, x: int, y: int) -> CheckerType:
        return self.__checkers[y][x].type

    def at(self, x: int, y: int) -> Checker:
        return self.__checkers[y][x]

    def is_within(self, x: int, y: int) -> bool:
        return 0 <= x < self.x_size and 0 <= y < self.y_size

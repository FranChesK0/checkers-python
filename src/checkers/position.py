from typing import Tuple


class Position:
    def __init__(self, x: int = -1, y: int = -1) -> None:
        self.__x = x
        self.__y = y

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Position):
            return NotImplemented
        return self.x == value.x and self.y == value.y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y


# Possible move offsets for checkers
MOVE_OFFSETS: Tuple[Position, Position, Position, Position] = (
    Position(-1, -1),
    Position(1, -1),
    Position(-1, 1),
    Position(1, 1),
)

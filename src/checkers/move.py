from .position import Position


class Move:
    def __init__(self, from_: Position = Position(), to: Position = Position()) -> None:
        self.__from = from_
        self.__to = to

    def __repr__(self) -> str:
        return f"{self.from_.x}:{self.from_.y} -> {self.to.x}:{self.to.y}"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Move):
            return NotImplemented
        return self.from_ == value.from_ and self.to == value.to

    @property
    def from_(self) -> Position:
        return self.__from

    @property
    def to(self) -> Position:
        return self.__to

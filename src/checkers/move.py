import dataclasses

from .position import Position


@dataclasses.dataclass()
class Move:
    def __init__(self, from_: Position = Position(), to: Position = Position()) -> None:
        self.__from = from_
        self.__to = to

    @property
    def from_(self) -> Position:
        return self.__from

    @property
    def to(self) -> Position:
        return self.__to

    def __repr__(self) -> str:
        return f"{self.from_.x}:{self.from_.y} -> {self.to.x}:{self.to.y}"

    def __str__(self) -> str:
        return self.__repr__()

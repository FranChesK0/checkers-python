import dataclasses


@dataclasses.dataclass(frozen=True)
class Position:
    def __init__(self, x: int = -1, y: int = -1) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

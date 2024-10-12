import enum


class SideType(enum.Enum):
    WHITE: int = enum.auto()
    BLACK: int = enum.auto()

    def opposite(side: "SideType") -> "SideType":
        match side:
            case SideType.WHITE:
                return SideType.BLACK
            case SideType.BLACK:
                return SideType.WHITE
            case _:
                raise ValueError()

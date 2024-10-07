import dataclasses
from typing import Tuple, NamedTuple

from .enums import SideType, CheckerType
from .point import Point


class BoardColors(NamedTuple):
    Light: str
    Dark: str


@dataclasses.dataclass(frozen=True)
class GameConfig:
    PLAYER_SIDE: SideType = SideType.WHITE  # side which player starts
    MAX_PREDICTION_DEPTH: int = 3  # number of steps that counts


@dataclasses.dataclass(frozen=True)
class RenderParams:
    X_SIZE: int = 8
    Y_SIZE: int = 8
    CELL_SIZE: int = 74  # in px
    ANIMATION_VELOCITY: int = 4  # grater == faster
    BORDER_WIDTH: int = 2 * 2  # preferably it should be even


@dataclasses.dataclass(frozen=True)
class Colors:
    FIELD_COLORS: BoardColors = BoardColors(
        "#E7CFA9", "#927456"
    )  # colors of the game board
    HOVER_BORDER_COLOR: str = "#54B346"  # color of the border when hovering
    SELECT_BORDER_COLOR: str = "#944444"  # color of the border when selected
    POSSIBLE_MOVE_COLOR: str = "#944444"  # color of the possible moves


# Possible move offsets for checkers
MOVE_OFFSETS: Tuple[Point, Point, Point, Point] = (
    Point(-1, -1),
    Point(1, -1),
    Point(-1, 1),
    Point(1, 1),
)

# Tuple of white and black checkers type (man, king)
WHITE_CHECKERS: Tuple[CheckerType, CheckerType] = (
    CheckerType.WHITE_MAN,
    CheckerType.WHITE_KING,
)
BLACK_CHECKERS: Tuple[CheckerType, CheckerType] = (
    CheckerType.BLACK_MAN,
    CheckerType.BLACK_KING,
)

GAME_CONFIG: GameConfig = GameConfig()
RENDER_PARAMS: RenderParams = RenderParams()
COLORS: Colors = Colors()

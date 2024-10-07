from typing import List

from .enums import SideType, CheckerType
from .point import Point

# Side which player starts
PLAYER_SIDE: SideType = SideType.WHITE

# Field size
X_SIZE: int = 8
Y_SIZE: int = 8
# Cell size in px
CELL_SIZE: int = 75

# Animation velocity (grater == faster)
ANIMATION_SPEED: int = 4

# Number of steps that counts
MAX_PREDICTION_DEPTH: int = 3

# Border width (preferably it should be even)
BORDER_WIDTH: int = 2 * 2

# Color of the game board
FIELD_COLORS: List[str] = ["#E7CFA9", "#927456"]
# Color of the border when hovering
HOVER_BORDER_COLOR: str = "#54B346"
# Color of the border when selected
SELECT_BORDER_COLOR: str = "$944444"
# Color of possible moves
POSSIBLE_MOVE_COLOR: str = "#944444"

# Possible move offsets for checkers
MOVE_OFFSETS: List[Point] = [Point(-1, -1), Point(1, -1), Point(-1, 1), Point(1, 1)]

# List of white and black checkers type [man, king]
WHITE_CHECKERS = [CheckerType.WHITE_MAN, CheckerType.WHITE_KING]
BLACK_CHECKERS = [CheckerType.BLACK_MAN, CheckerType.BLACK_KING]

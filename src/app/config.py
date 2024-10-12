from typing import NamedTuple

from checkers import SideType


class BoardColors(NamedTuple):
    Light: str = "#E7CFA9"
    Dark: str = "#927456"


class AppConfig(NamedTuple):
    WINDOW_TITLE: str = "Checkers"
    PLAYER_SIDE: SideType = SideType.WHITE  # side which players starts
    MAX_PREDICTION_DEPTH: int = 3  # number of steps that count


class RenderParams(NamedTuple):
    X_SIZE: int = 8
    Y_SIZE: int = 8
    CELL_SIZE: int = 74  # in px
    ANIMATION_VELOCITY: int = 4  # grater = faster
    BORDER_WIDTH: int = 2 * 2  # preferably it should be even


class Colors(NamedTuple):
    BOARD_COLORS: BoardColors = BoardColors()  # colors of the game board
    HOVER_BORDER_COLOR: str = "#54B346"
    SELECT_BORDER_COLOR: str = "#944444"
    POSSIBLE_MOVE_COLOR: str = "#944444"


app_config = AppConfig()
render_params = RenderParams()
colors = Colors()


def get_app_config() -> AppConfig:
    return app_config


def get_render_params() -> RenderParams:
    return render_params


def get_colors() -> Colors:
    return colors

from time import sleep
from typing import Dict, Tuple
from pathlib import Path
from tkinter import Tk, Event, Canvas, PhotoImage, messagebox

from PIL import Image, ImageTk

from checkers import (
    BLACK_CHECKERS,
    WHITE_CHECKERS,
    Move,
    Board,
    Position,
    SideType,
    CheckerType,
)

from .config import get_colors, get_app_config, get_render_params

APP_CONFIG = get_app_config()
RENDER_PARAMS = get_render_params()
COLORS = get_colors()


class App:
    def __init__(self) -> None:
        self.__window = Tk()
        self.__window.title(APP_CONFIG.WINDOW_TITLE)
        self.__window.resizable(False, False)
        self.__window.iconphoto(False, PhotoImage(file=Path("assets", "icon.png")))

        self.__canvas = Canvas(
            self.__window,
            width=RENDER_PARAMS.X_SIZE * RENDER_PARAMS.CELL_SIZE,
            height=RENDER_PARAMS.Y_SIZE * RENDER_PARAMS.CELL_SIZE,
        )
        self.__canvas.pack()

        self.__canvas.bind("<Motion>", self.__handle_mouse_move)
        self.__canvas.bind("<Button-1>", self.__handle_mouse_clicked)

        self.__images: Dict[CheckerType, ImageTk.PhotoImage]
        self.__player_turn: bool
        self.__hovered_cell: Position
        self.__selected_cell: Position
        self.__animated_cell: Position
        self.__board: Board

        self.__setup()

    def mainloop(self) -> None:
        self.__window.mainloop()

    def __handle_mouse_move(self, event: Event) -> None:
        x, y = event.x // RENDER_PARAMS.CELL_SIZE, event.y // RENDER_PARAMS.CELL_SIZE
        if x != self.__hovered_cell.x or y != self.__hovered_cell.y:
            self.__hovered_cell = Position(x, y)

            if self.__player_turn:
                self.__draw()

    def __handle_mouse_clicked(self, event: Event) -> None:
        if not self.__player_turn:
            return

        x, y = event.x // RENDER_PARAMS.CELL_SIZE, event.y // RENDER_PARAMS.CELL_SIZE
        if not self.__board.is_within(x, y):
            return

        player_checkers: Tuple[CheckerType, CheckerType]
        if APP_CONFIG.PLAYER_SIDE == SideType.WHITE:
            player_checkers = WHITE_CHECKERS
        elif APP_CONFIG.PLAYER_SIDE == SideType.BLACK:
            player_checkers = BLACK_CHECKERS
        else:
            return

        if self.__board.type_at(x, y) in player_checkers:
            self.__selected_cell = Position(x, y)
            self.__draw()
        elif self.__player_turn:
            move = Move(
                Position(self.__selected_cell.x, self.__selected_cell.y), Position(x, y)
            )
            if move in self.__board.get_moves(APP_CONFIG.PLAYER_SIDE):
                self.__handle_player_turn(move)
                if not self.__player_turn:
                    self.__handle_opponent_turn()

    def __setup(self) -> None:
        self.__board = Board(RENDER_PARAMS.X_SIZE, RENDER_PARAMS.Y_SIZE)
        self.__player_turn = True
        self.__hovered_cell = Position()
        self.__selected_cell = Position()
        self.__animated_cell = Position()

        self.__init_images()
        self.__draw()

        if APP_CONFIG.PLAYER_SIDE == SideType.BLACK:
            self.__handle_opponent_turn()

    def __init_images(self) -> None:
        self.__images = {
            CheckerType.WHITE_MAN: ImageTk.PhotoImage(
                Image.open(Path("assets", "white-man.png")).resize(
                    (RENDER_PARAMS.CELL_SIZE, RENDER_PARAMS.CELL_SIZE),
                    Image.Resampling.LANCZOS,
                )
            ),
            CheckerType.BLACK_MAN: ImageTk.PhotoImage(
                Image.open(Path("assets", "black-man.png")).resize(
                    (RENDER_PARAMS.CELL_SIZE, RENDER_PARAMS.CELL_SIZE),
                    Image.Resampling.LANCZOS,
                )
            ),
            CheckerType.WHITE_KING: ImageTk.PhotoImage(
                Image.open(Path("assets", "white-king.png")).resize(
                    (RENDER_PARAMS.CELL_SIZE, RENDER_PARAMS.CELL_SIZE),
                    Image.Resampling.LANCZOS,
                )
            ),
            CheckerType.BLACK_KING: ImageTk.PhotoImage(
                Image.open(Path("assets", "black-king.png")).resize(
                    (RENDER_PARAMS.CELL_SIZE, RENDER_PARAMS.CELL_SIZE),
                    Image.Resampling.LANCZOS,
                )
            ),
        }

    def __draw(self) -> None:
        self.__canvas.delete("all")
        self.__draw_board_grid()
        self.__draw_checkers()

    def __handle_player_turn(self, move: Move) -> None:
        self.__player_turn = False
        has_killed_checker = self.__handle_move(move)
        required_moves = list(
            filter(
                lambda req: move.to.x == req.from_.x and move.to.y == req.from_.y,
                self.__board.get_required_moves(APP_CONFIG.PLAYER_SIDE),
            )
        )
        if has_killed_checker and required_moves:
            self.__player_turn = True
        self.__selected_cell = Position()

    def __handle_opponent_turn(self) -> None:
        self.__player_turn = False
        optimal_move = self.__board.get_optimal_move(
            SideType.opposite(APP_CONFIG.PLAYER_SIDE), APP_CONFIG.MAX_PREDICTION_DEPTH
        )
        for move in optimal_move:
            self.__handle_move(move)
        self.__player_turn = True
        self.__check_game_over()

    def __draw_board_grid(self) -> None:
        board_colors = [COLORS.BOARD_COLORS.Light, COLORS.BOARD_COLORS.Dark]
        for y in range(self.__board.y_size):
            for x in range(self.__board.x_size):
                self.__canvas.create_rectangle(
                    x * RENDER_PARAMS.CELL_SIZE,
                    y * RENDER_PARAMS.CELL_SIZE,
                    x * RENDER_PARAMS.CELL_SIZE + RENDER_PARAMS.CELL_SIZE,
                    y * RENDER_PARAMS.CELL_SIZE + RENDER_PARAMS.CELL_SIZE,
                    fill=board_colors[(y + x) % 2],
                    width=0,
                )

                if x == self.__selected_cell.x and y == self.__selected_cell.y:
                    self.__canvas.create_rectangle(
                        x * RENDER_PARAMS.CELL_SIZE + RENDER_PARAMS.BORDER_WIDTH // 2,
                        y * RENDER_PARAMS.CELL_SIZE + RENDER_PARAMS.BORDER_WIDTH // 2,
                        x * RENDER_PARAMS.CELL_SIZE
                        + RENDER_PARAMS.CELL_SIZE
                        - RENDER_PARAMS.BORDER_WIDTH // 2,
                        y * RENDER_PARAMS.CELL_SIZE
                        + RENDER_PARAMS.CELL_SIZE
                        - RENDER_PARAMS.BORDER_WIDTH // 2,
                        outline=COLORS.SELECT_BORDER_COLOR,
                        width=RENDER_PARAMS.BORDER_WIDTH,
                    )
                elif x == self.__hovered_cell.x and y == self.__hovered_cell.y:
                    self.__canvas.create_rectangle(
                        x * RENDER_PARAMS.CELL_SIZE + RENDER_PARAMS.BORDER_WIDTH // 2,
                        y * RENDER_PARAMS.CELL_SIZE + RENDER_PARAMS.BORDER_WIDTH // 2,
                        x * RENDER_PARAMS.CELL_SIZE
                        + RENDER_PARAMS.CELL_SIZE
                        - RENDER_PARAMS.BORDER_WIDTH // 2,
                        y * RENDER_PARAMS.CELL_SIZE
                        + RENDER_PARAMS.CELL_SIZE
                        - RENDER_PARAMS.BORDER_WIDTH // 2,
                        outline=COLORS.HOVER_BORDER_COLOR,
                        width=RENDER_PARAMS.BORDER_WIDTH,
                    )

                if self.__selected_cell:
                    player_moves_list = self.__board.get_moves(APP_CONFIG.PLAYER_SIDE)
                    for move in player_moves_list:
                        if (
                            self.__selected_cell.x == move.from_.x
                            and self.__selected_cell.y == move.from_.y
                        ):
                            self.__canvas.create_oval(
                                move.to.x * RENDER_PARAMS.CELL_SIZE
                                + RENDER_PARAMS.CELL_SIZE / 3,
                                move.to.y * RENDER_PARAMS.CELL_SIZE
                                + RENDER_PARAMS.CELL_SIZE / 3,
                                move.to.x * RENDER_PARAMS.CELL_SIZE
                                + (RENDER_PARAMS.CELL_SIZE - RENDER_PARAMS.CELL_SIZE / 3),
                                move.to.y * RENDER_PARAMS.CELL_SIZE
                                + (RENDER_PARAMS.CELL_SIZE - RENDER_PARAMS.CELL_SIZE / 3),
                                fill=COLORS.POSSIBLE_MOVE_COLOR,
                                width=0,
                            )

    def __draw_checkers(self) -> None:
        for y in range(self.__board.y_size):
            for x in range(self.__board.x_size):
                if self.__board.type_at(x, y) != CheckerType.NONE and not (
                    x == self.__animated_cell.x and y == self.__animated_cell.y
                ):
                    self.__canvas.create_image(
                        x * RENDER_PARAMS.CELL_SIZE,
                        y * RENDER_PARAMS.CELL_SIZE,
                        image=self.__images.get(self.__board.type_at(x, y)),
                        anchor="nw",
                        tag="checkers",
                    )

    def __handle_move(self, move: Move) -> bool:
        self.__animate_move(move)
        has_killed = self.__board.handle_move(move)
        self.__draw()
        return has_killed

    def __check_game_over(self) -> None:
        game_over, side = self.__board.is_game_over()
        if game_over:
            messagebox.showinfo(
                "Game Over", "White Wins" if side == SideType.WHITE else "Black Wins"
            )
            self.__setup()

    def __animate_move(self, move: Move) -> None:
        self.__animated_cell = Position(move.from_.x, move.from_.y)
        self.__draw()

        animated_checker = self.__canvas.create_image(
            move.from_.x * RENDER_PARAMS.CELL_SIZE,
            move.from_.y * RENDER_PARAMS.CELL_SIZE,
            image=self.__images.get(self.__board.type_at(move.from_.x, move.from_.y)),
            anchor="nw",
            tag="animated_checker",
        )

        dx = 1 if move.from_.x < move.to.x else -1
        dy = 1 if move.from_.y < move.to.y else -1

        for _ in range(abs(move.from_.x - move.to.x)):
            for _ in range(100 // RENDER_PARAMS.ANIMATION_VELOCITY):
                self.__canvas.move(
                    animated_checker,
                    RENDER_PARAMS.ANIMATION_VELOCITY / 100 * RENDER_PARAMS.CELL_SIZE * dx,
                    RENDER_PARAMS.ANIMATION_VELOCITY / 100 * RENDER_PARAMS.CELL_SIZE * dy,
                )
                self.__canvas.update()
                sleep(0.01)

        self.__animated_cell = Position()

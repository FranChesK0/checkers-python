from math import inf
from time import sleep
from random import choice
from typing import List, Tuple, Optional
from pathlib import Path
from tkinter import Event, Canvas, messagebox

from PIL import Image, ImageTk

from .move import Move
from .enums import SideType, CheckerType
from .filed import Field
from .point import Point
from .constants import (
    COLORS,
    GAME_CONFIG,
    MOVE_OFFSETS,
    RENDER_PARAMS,
    BLACK_CHECKERS,
    WHITE_CHECKERS,
)


class Game:
    def __init__(self, canvas: Canvas, x_field_size: int, y_field_size: int) -> None:
        self.__canvas = canvas
        self.__field = Field(x_field_size, y_field_size)

        self.__player_turn = True

        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()

        self.__init_images()
        self.__draw()

        if GAME_CONFIG.PLAYER_SIDE == SideType.BLACK:
            self.__handle_opponent_turn()

    def mouse_move(self, event: Event) -> None:
        x, y = event.x // RENDER_PARAMS.CELL_SIZE, event.y // RENDER_PARAMS.CELL_SIZE
        if x != self.__hovered_cell.x or y != self.__hovered_cell.y:
            self.__hovered_cell = Point(x, y)

            if self.__player_turn:
                self.__draw()

    def mouse_down(self, event: Event) -> None:
        if not self.__player_turn:
            return

        x, y = event.x // RENDER_PARAMS.CELL_SIZE, event.y // RENDER_PARAMS.CELL_SIZE
        if not (self.__field.is_within(x, y)):
            return

        player_checkers: Tuple[CheckerType, CheckerType]
        if GAME_CONFIG.PLAYER_SIDE == SideType.WHITE:
            player_checkers = WHITE_CHECKERS
        elif GAME_CONFIG.PLAYER_SIDE == SideType.BLACK:
            player_checkers == BLACK_CHECKERS
        else:
            return

        if self.__field.type_at(x, y) in player_checkers:
            self.__selected_cell = Point(x, y)
            self.__draw()
        elif self.__player_turn:
            move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)
            if move in self.__get_moves_list(GAME_CONFIG.PLAYER_SIDE):
                self.__handle_player_turn(move)
                if not self.__player_turn:
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

    def __animate_move(self, move: Move) -> None:
        self.__animated_cell = Point(move.from_x, move.from_y)
        self.__draw()

        animated_checker = self.__canvas.create_image(
            move.from_x * RENDER_PARAMS.CELL_SIZE,
            move.from_y * RENDER_PARAMS.CELL_SIZE,
            image=self.__images.get(self.__field.type_at(move.from_x, move.from_y)),
            anchor="nw",
            tag="animated_checker",
        )

        dx = 1 if move.from_x < move.to_x else -1
        dy = 1 if move.from_y < move.to_y else -1

        for _ in range(abs(move.from_x - move.to_x)):
            for _ in range(100 // RENDER_PARAMS.ANIMATION_VELOCITY):
                self.__canvas.move(
                    animated_checker,
                    RENDER_PARAMS.ANIMATION_VELOCITY
                    / 100
                    * RENDER_PARAMS.CELL_SIZE
                    * dx,
                    RENDER_PARAMS.ANIMATION_VELOCITY
                    / 100
                    * RENDER_PARAMS.CELL_SIZE
                    * dy,
                )
                self.__canvas.update()
                sleep(0.01)

        self.__animated_cell = Point()

    def __draw(self) -> None:
        self.__canvas.delete("all")
        self.__draw_field_grid()
        self.__draw_checkers()

    def __draw_field_grid(self) -> None:
        board_colors = [COLORS.FIELD_COLORS.Light, COLORS.FIELD_COLORS.Dark]
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
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
                    player_moves_list = self.__get_moves_list(GAME_CONFIG.PLAYER_SIDE)
                    for move in player_moves_list:
                        if (
                            self.__selected_cell.x == move.from_x
                            and self.__selected_cell.y == move.from_y
                        ):
                            self.__canvas.create_oval(
                                move.to_x * RENDER_PARAMS.CELL_SIZE
                                + RENDER_PARAMS.CELL_SIZE / 3,
                                move.to_y * RENDER_PARAMS.CELL_SIZE
                                + RENDER_PARAMS.CELL_SIZE / 3,
                                move.to_x * RENDER_PARAMS.CELL_SIZE
                                + (
                                    RENDER_PARAMS.CELL_SIZE
                                    - RENDER_PARAMS.CELL_SIZE / 3
                                ),
                                move.to_y * RENDER_PARAMS.CELL_SIZE
                                + (
                                    RENDER_PARAMS.CELL_SIZE
                                    - RENDER_PARAMS.CELL_SIZE / 3
                                ),
                                fill=COLORS.POSSIBLE_MOVE_COLOR,
                                width=0,
                            )

    def __draw_checkers(self) -> None:
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                if self.__field.type_at(x, y) != CheckerType.NONE and not (
                    x == self.__animated_cell.x and y == self.__animated_cell.y
                ):
                    self.__canvas.create_image(
                        x * RENDER_PARAMS.CELL_SIZE,
                        y * RENDER_PARAMS.CELL_SIZE,
                        image=self.__images.get(self.__field.type_at(x, y)),
                        anchor="nw",
                        tag="checkers",
                    )

    def __handle_move(self, move: Move, draw: bool = True) -> bool:
        if draw:
            self.__animate_move(move)

        if (
            move.to_y == 0
            and self.__field.type_at(move.from_x, move.from_y) == CheckerType.WHITE_MAN
        ):
            self.__field.at(move.from_x, move.from_y).change_type(
                CheckerType.WHITE_KING
            )
        elif (
            move.to_y == self.__field.y_size - 1
            and self.__field.type_at(move.from_x, move.from_y) == CheckerType.BLACK_MAN
        ):
            self.__field.at(move.from_x, move.from_y).change_type(
                CheckerType.BLACK_KING
            )

        self.__field.at(move.to_x, move.to_y).change_type(
            self.__field.type_at(move.from_x, move.from_y)
        )
        self.__field.at(move.from_x, move.from_y).change_type(CheckerType.NONE)

        dx = -1 if move.from_x < move.to_x else 1
        dy = -1 if move.from_y < move.to_y else 1

        has_killed_checker = False
        x, y = move.to_x, move.to_y
        while x != move.from_x or y != move.from_y:
            x += dx
            y += dy
            if self.__field.type_at(x, y) != CheckerType.NONE:
                self.__field.at(x, y).change_type(CheckerType.NONE)
                has_killed_checker = True

        if draw:
            self.__draw()

        return has_killed_checker

    def __handle_player_turn(self, move: Move) -> None:
        self.__player_turn = False

        has_killed_checker = self.__handle_move(move)
        required_moves_list = list(
            filter(
                lambda required_move: move.to_x == required_move.from_x
                and move.to_y == required_move.from_y,
                self.__get_required_moves_list(GAME_CONFIG.PLAYER_SIDE),
            )
        )

        if has_killed_checker and required_moves_list:
            self.__player_turn = True

        self.__selected_cell = Point()

    def __handle_opponent_turn(self) -> None:
        self.__player_turn = False

        optimal_moves_list = self.__count_optimal_moves(
            SideType.opposite(GAME_CONFIG.PLAYER_SIDE)
        )

        for move in optimal_moves_list:
            self.__handle_move(move)

        self.__player_turn = True
        self.__check_game_over()

    def __check_game_over(self) -> None:
        game_over = False

        white_moves_list = self.__get_moves_list(SideType.WHITE)
        if not white_moves_list:
            messagebox.showinfo("Game Over", "Black Wins")
            game_over = True

        black_moves_list = self.__get_moves_list(SideType.BLACK)
        if not black_moves_list:
            messagebox.showinfo("Game Over", "White Wins")
            game_over = True

        if game_over:
            self = Game(self.__canvas, self.__field.x_size, self.__field.y_size)

    def __count_optimal_moves(self, side: SideType) -> List[Move]:
        best_result: float = 0.0
        optimal_moves: List[List[Move]] = []
        predicted_move_list = self.__get_possible_move_list(side)

        if predicted_move_list:
            filed_copy = Field.copy(self.__field)
            for moves in predicted_move_list:
                for move in moves:
                    self.__handle_move(move, draw=False)

                    try:
                        if side == SideType.WHITE:
                            result = self.__field.white_score / self.__field.black_score
                        elif side == SideType.BLACK:
                            result = self.__field.black_score / self.__field.white_score
                    except ZeroDivisionError:
                        result = inf

                    if result > best_result:
                        best_result = result
                        optimal_moves.clear()
                        optimal_moves.append(moves)
                    elif result == best_result:
                        optimal_moves.append(moves)

                    self.__field = Field.copy(filed_copy)

        optimal_move = []
        if optimal_moves:
            for move in choice(optimal_moves):
                if (
                    side == SideType.WHITE
                    and self.__field.type_at(move.from_x, move.from_y) in BLACK_CHECKERS
                ):
                    break
                elif (
                    side == SideType.BLACK
                    and self.__field.type_at(move.from_x, move.from_y) in WHITE_CHECKERS
                ):
                    break
                optimal_move.append(move)

        return optimal_move

    def __get_possible_move_list(
        self,
        side: SideType,
        prediction_depth: int = 0,
        all_moves_list: Optional[List[List[Move]]] = None,
        moves_list: Optional[List[Move]] = None,
        required_moves_list: Optional[List[Move]] = None,
    ) -> List[List[Move]]:
        all_moves: List[List[Move]] = all_moves_list or []
        moves: List[Move] = moves_list or []
        required_moves: List[Move] = required_moves_list or []

        if moves:
            all_moves.append(moves)
        else:
            all_moves.clear()

        if required_moves:
            moves = required_moves
        else:
            moves = self.__get_moves_list(side)

        if moves and prediction_depth < GAME_CONFIG.MAX_PREDICTION_DEPTH:
            field_copy = Field.copy(self.__field)
            for move in moves:
                has_killed_checker = self.__handle_move(move, draw=False)
                required_moves = list(
                    filter(
                        lambda required_move: move.to_x == required_move.from_x
                        and move.to_y == required_move.from_y,
                        self.__get_required_moves_list(side),
                    )
                )

                if has_killed_checker and required_moves:
                    all_moves = self.__get_possible_move_list(
                        side,
                        prediction_depth,
                        all_moves,
                        moves + [move],
                        required_moves,
                    )
                else:
                    all_moves = self.__get_possible_move_list(
                        SideType.opposite(side),
                        prediction_depth + 1,
                        all_moves,
                        moves + [move],
                    )

                self.__field = Field.copy(field_copy)

        return all_moves

    def __get_moves_list(self, side: SideType) -> List[Move]:
        moves_list = self.__get_required_moves_list(side)
        if not moves_list:
            moves_list = self.__get_optional_moves_list(side)
        return moves_list

    def __get_required_moves_list(self, side: SideType) -> List[Move]:
        moves_list = []

        if side == SideType.WHITE:
            friendly_checkers = WHITE_CHECKERS
            opponent_checkers = BLACK_CHECKERS
        elif side == SideType.BLACK:
            friendly_checkers = BLACK_CHECKERS
            opponent_checkers = WHITE_CHECKERS
        else:
            return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # if man checker
                if self.__field.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS:
                        if not self.__field.is_within(
                            x + offset.x * 2, y + offset.y * 2
                        ):
                            continue
                        if (
                            self.__field.type_at(x + offset.x, y + offset.y)
                            in opponent_checkers
                            and self.__field.type_at(x + offset.x * 2, y + offset.y * 2)
                            == CheckerType.NONE
                        ):
                            moves_list.append(
                                Move(x, y, x + offset.x * 2, y + offset.y * 2)
                            )
                # if king checker
                elif self.__field.type_at(x, y) == friendly_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not self.__field.is_within(
                            x + offset.x * 2, y + offset.y * 2
                        ):
                            continue

                        has_opponent_checker_on_way = False

                        for shift in range(1, self.__field.size):
                            if not self.__field.is_within(
                                x + offset.x * shift, y + offset.y * shift
                            ):
                                continue

                            if not has_opponent_checker_on_way:
                                if (
                                    self.__field.type_at(
                                        x + offset.x * shift, y + offset.y * shift
                                    )
                                    in opponent_checkers
                                ):
                                    has_opponent_checker_on_way = True
                                    continue
                                elif (
                                    self.__field.type_at(
                                        x + offset.x * shift, y + offset.y * shift
                                    )
                                    in friendly_checkers
                                ):
                                    break

                            if has_opponent_checker_on_way:
                                if (
                                    self.__field.type_at(
                                        x + offset.x * shift, y + offset.y * shift
                                    )
                                    == CheckerType.NONE
                                ):
                                    moves_list.append(
                                        Move(
                                            x,
                                            y,
                                            x + offset.x * shift,
                                            y + offset.y * shift,
                                        )
                                    )
                                else:
                                    break

        return moves_list

    def __get_optional_moves_list(self, side: SideType) -> List[Move]:
        moves_list = []

        if side == SideType.WHITE:
            friendly_checkers = WHITE_CHECKERS
        elif side == SideType.BLACK:
            friendly_checkers = BLACK_CHECKERS
        else:
            return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # if man checker
                if self.__field.type_at(x, y) == friendly_checkers[0]:
                    for offset in (
                        MOVE_OFFSETS[:2] if side == SideType.WHITE else MOVE_OFFSETS[2:]
                    ):
                        if not self.__field.is_within(x + offset.x, y + offset.y):
                            continue
                        if (
                            self.__field.type_at(x + offset.x, y + offset.y)
                            == CheckerType.NONE
                        ):
                            moves_list.append(Move(x, y, x + offset.x, y + offset.y))
                # if king checker
                elif self.__field.type_at(x, y) == friendly_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not self.__field.is_within(x + offset.x, y + offset.y):
                            continue
                        for shift in range(1, self.__field.size):
                            if not self.__field.is_within(
                                x + offset.x * shift, y + offset.y * shift
                            ):
                                continue
                            if (
                                self.__field.type_at(
                                    x + offset.x * shift, y + offset.y * shift
                                )
                                == CheckerType.NONE
                            ):
                                moves_list.append(
                                    Move(
                                        x, y, x + offset.x * shift, y + offset.y * shift
                                    )
                                )
                            else:
                                break

        return moves_list

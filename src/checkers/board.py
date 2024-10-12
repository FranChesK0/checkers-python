from math import inf
from random import choice
from typing import List, Tuple, Optional
from functools import reduce

from .move import Move
from .side import SideType
from .checker import BLACK_CHECKERS, WHITE_CHECKERS, Checker, CheckerType
from .position import MOVE_OFFSETS, Position


class Board:
    def __init__(self, x_size: int, y_size: int) -> None:
        self.__x_size = x_size
        self.__y_size = y_size
        self.__checkers: List[List[Checker]]

        self.__generate()

    def __repr__(self) -> str:
        board = ""
        for y in range(self.y_size):
            for x in range(self.x_size):
                ct = self.type_at(x, y)
                if ct == CheckerType.NONE:
                    board += "-- "
                elif ct == CheckerType.WHITE_MAN:
                    board += "WM "
                elif ct == CheckerType.WHITE_KING:
                    board += "WK "
                elif ct == CheckerType.BLACK_MAN:
                    board += "BM "
                else:
                    board += "BK "
            board += "\n"
        return f"x[{self.x_size}]:y[{self.y_size}]\n{board}"

    @classmethod
    def copy(cls, board: "Board") -> "Board":
        board_copy = cls(board.x_size, board.y_size)
        for y in range(board.y_size):
            for x in range(board.x_size):
                board_copy.at(x, y).type = board.type_at(x, y)
        return board_copy

    @property
    def x_size(self) -> int:
        return self.__x_size

    @property
    def y_size(self) -> int:
        return self.__y_size

    @property
    def size(self) -> int:
        return max(self.x_size, self.y_size)

    @property
    def white_checkers_count(self) -> int:
        return self.__checkers_count(WHITE_CHECKERS)

    @property
    def black_checkers_count(self) -> int:
        return self.__checkers_count(BLACK_CHECKERS)

    @property
    def white_score(self) -> int:
        return self.__score(CheckerType.WHITE_MAN, CheckerType.WHITE_KING)

    @property
    def black_score(self) -> int:
        return self.__score(CheckerType.BLACK_MAN, CheckerType.BLACK_KING)

    def restore_copy(self, board: "Board") -> None:
        self.__x_size = board.x_size
        self.__y_size = board.y_size
        for y in range(board.y_size):
            for x in range(board.x_size):
                self.at(x, y).type = board.type_at(x, y)

    def is_within(self, x: int, y: int) -> bool:
        return 0 <= x < self.x_size and 0 <= y < self.y_size

    def at(self, x: int, y: int) -> Checker:
        return self.__checkers[y][x]

    def type_at(self, x: int, y: int) -> CheckerType:
        return self.at(x, y).type

    def handle_move(self, move: Move) -> bool:
        if (
            move.to.y == 0
            and self.type_at(move.from_.x, move.from_.y) == CheckerType.WHITE_MAN
        ):
            self.at(move.from_.x, move.from_.y).type = CheckerType.WHITE_KING
        elif (
            move.to.y == self.y_size - 1
            and self.type_at(move.from_.x, move.from_.y) == CheckerType.BLACK_MAN
        ):
            self.at(move.from_.x, move.from_.y).type = CheckerType.BLACK_KING
        self.at(move.to.x, move.to.y).type = self.type_at(move.from_.x, move.from_.y)
        self.at(move.from_.x, move.from_.y).type = CheckerType.NONE

        dx = -1 if move.from_.x < move.to.x else 1
        dy = -1 if move.from_.y < move.to.y else 1
        has_killed = False
        x, y = move.to.x, move.to.y
        while x != move.from_.x or y != move.from_.y:
            x += dx
            y += dy
            if self.type_at(x, y) != CheckerType.NONE:
                self.at(x, y).type = CheckerType.NONE
                has_killed = True
        return has_killed

    def is_game_over(self) -> Tuple[bool, Optional[SideType]]:
        white_moves = self.get_moves(SideType.WHITE)
        if not white_moves:
            return True, SideType.BLACK
        black_moves = self.get_moves(SideType.BLACK)
        if not black_moves:
            return True, SideType.WHITE
        return False, None

    def get_moves(self, side: SideType) -> List[Move]:
        moves = self.get_required_moves(side)
        if not moves:
            moves = self.__get_optional_moves(side)
        return moves

    def get_required_moves(self, side: SideType) -> List[Move]:
        required_moves: List[Move] = []
        man: CheckerType
        king: CheckerType
        if side == SideType.WHITE:
            man = CheckerType.WHITE_MAN
            king = CheckerType.WHITE_KING
            opponent_checkers = BLACK_CHECKERS
        elif side == SideType.BLACK:
            man = CheckerType.BLACK_MAN
            king = CheckerType.BLACK_KING
            opponent_checkers = WHITE_CHECKERS
        else:
            return required_moves

        for y in range(self.y_size):
            for x in range(self.x_size):
                if self.type_at(x, y) == man:
                    for offset in MOVE_OFFSETS:
                        x_offset = x + 2 * offset.x
                        y_offset = y + 2 * offset.y
                        if not self.is_within(x_offset, y_offset):
                            continue
                        if (
                            self.type_at(x + offset.x, y + offset.y) in opponent_checkers
                            and self.type_at(x_offset, y_offset) == CheckerType.NONE
                        ):
                            required_moves.append(
                                Move(Position(x, y), Position(x_offset, y_offset))
                            )
                elif self.type_at(x, y) == king:
                    for offset in MOVE_OFFSETS:
                        if not self.is_within(x + 2 * offset.x, y + 2 * offset.y):
                            continue
                        has_opponent_checker_on_way = False
                        for shift in range(1, self.size):
                            x_offset = x + shift * offset.x
                            y_offset = y + shift * offset.y
                            if not self.is_within(x_offset, y_offset):
                                continue
                            if not has_opponent_checker_on_way:
                                if self.type_at(x_offset, y_offset) in opponent_checkers:
                                    has_opponent_checker_on_way = True
                                    continue
                                elif self.type_at(x_offset, y_offset) in (man, king):
                                    break
                            if has_opponent_checker_on_way:
                                if self.type_at(x_offset, y_offset) == CheckerType.NONE:
                                    required_moves.append(
                                        Move(Position(x, y), Position(x_offset, y_offset))
                                    )
                                else:
                                    break

        return required_moves

    def get_optimal_move(self, side: SideType, max_prediction_depth: int) -> List[Move]:
        best_result = 0.0
        optimal_moves: List[List[Move]] = []
        possible_moves = self.__get_possible_moves(side, max_prediction_depth)

        if possible_moves:
            board_copy = Board.copy(self)
            for moves in possible_moves:
                for move in moves:
                    self.handle_move(move)
                    try:
                        if side == SideType.WHITE:
                            result = self.white_score / self.black_score
                        elif side == SideType.BLACK:
                            result = self.black_score / self.white_score
                    except ZeroDivisionError:
                        result = inf
                    if result > best_result:
                        best_result = result
                        optimal_moves.clear()
                        optimal_moves.append(moves)
                    elif result == best_result:
                        optimal_moves.append(moves)
                    self.restore_copy(board_copy)

        optimal_move: List[Move] = []
        if optimal_moves:
            for move in choice(optimal_moves):
                if (
                    side == SideType.WHITE
                    and self.type_at(move.from_.x, move.from_.y) in BLACK_CHECKERS
                ):
                    break
                elif (
                    side == SideType.BLACK
                    and self.type_at(move.from_.x, move.from_.y) in WHITE_CHECKERS
                ):
                    break
                optimal_move.append(move)
        return optimal_move

    def __generate(self) -> None:
        self.__checkers = [
            [Checker() for _ in range(self.x_size)] for _ in range(self.y_size)
        ]

        for y in range(self.y_size):
            for x in range(self.x_size):
                if (y + x) % 2:
                    if y < 3:
                        self.__checkers[y][x].type = CheckerType.BLACK_MAN
                    elif y >= self.y_size - 3:
                        self.__checkers[y][x].type = CheckerType.WHITE_MAN

    def __checkers_count(self, checkers: Tuple[CheckerType, ...]) -> int:
        return sum(
            reduce(lambda s, c: s + int(c.type in checkers), row, 0)
            for row in self.__checkers
        )

    def __score(self, man: CheckerType, king: CheckerType) -> int:
        return sum(
            reduce(
                lambda s, c: s + int(c.type == man) + 3 * int(c.type == king),
                row,
                0,
            )
            for row in self.__checkers
        )

    def __get_optional_moves(self, side: SideType) -> List[Move]:
        moves: List[Move] = []
        man: CheckerType
        king: CheckerType
        if side == SideType.WHITE:
            man = CheckerType.WHITE_MAN
            king = CheckerType.WHITE_KING
        elif side == SideType.BLACK:
            man = CheckerType.BLACK_MAN
            king = CheckerType.BLACK_KING
        else:
            return moves

        for y in range(self.y_size):
            for x in range(self.x_size):
                if self.type_at(x, y) == man:
                    for offset in (
                        MOVE_OFFSETS[:2] if side == SideType.WHITE else MOVE_OFFSETS[2:]
                    ):
                        x_offset = x + offset.x
                        y_offset = y + offset.y
                        if not self.is_within(x_offset, y_offset):
                            continue
                        if self.type_at(x_offset, y_offset) == CheckerType.NONE:
                            moves.append(
                                Move(Position(x, y), Position(x_offset, y_offset))
                            )
                elif self.type_at(x, y) == king:
                    for offset in MOVE_OFFSETS:
                        if not self.is_within(x + offset.x, y + offset.y):
                            continue
                        for shift in range(1, self.size):
                            x_offset = x + shift * offset.x
                            y_offset = y + shift * offset.y
                            if not self.is_within(x_offset, y_offset):
                                continue
                            if self.type_at(x_offset, y_offset) == CheckerType.NONE:
                                moves.append(
                                    Move(Position(x, y), Position(x_offset, y_offset))
                                )
                            else:
                                break

        return moves

    def __get_possible_moves(
        self,
        side: SideType,
        max_prediction_depth: int,
        prediction_depth: int = 0,
        all_moves: List[List[Move]] = [],
        current_moves: List[Move] = [],
        required_moves: List[Move] = [],
    ) -> List[List[Move]]:
        if current_moves:
            all_moves.append(current_moves)
        else:
            all_moves.clear()
        if required_moves:
            moves = required_moves
        else:
            moves = self.get_moves(side)
        if moves and prediction_depth < max_prediction_depth:
            board_copy = Board.copy(self)
            for move in moves:
                has_killed = self.handle_move(move)
                required_moves = list(
                    filter(
                        lambda req: move.to.x == req.from_.x and move.to.y == req.from_.y,
                        self.get_required_moves(side),
                    )
                )
                if has_killed and required_moves:
                    self.__get_possible_moves(
                        side,
                        max_prediction_depth,
                        prediction_depth,
                        all_moves,
                        current_moves + [move],
                        required_moves,
                    )
                else:
                    self.__get_possible_moves(
                        SideType.opposite(side),
                        max_prediction_depth,
                        prediction_depth + 1,
                        all_moves,
                        current_moves + [move],
                    )
                self.restore_copy(board_copy)
        return all_moves

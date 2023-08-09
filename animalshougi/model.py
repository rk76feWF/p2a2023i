import enum

Direction = enum.Enum(
    "Direction",
    ["FORWARD", "FORWARD_CROSS", "HORIZONTAL", "BACKWARD_CROSS", "BACKWARD"],
)


@enum.unique
class Piece(enum.Enum):
    """An enum of piece animal."""

    LION = enum.auto()
    GIRAFFE = enum.auto()
    ELEPHANT = enum.auto()
    CHICK = enum.auto()
    HEN = enum.auto()

    def can_move_toward(self, dir: Direction | None) -> bool:
        """Returns whether `self` can move toward `dir` or not."""
        if self is Piece.LION:
            return (
                dir is Direction.FORWARD
                or dir is Direction.FORWARD_CROSS
                or dir is Direction.HORIZONTAL
                or dir is Direction.BACKWARD_CROSS
                or dir is Direction.BACKWARD
            )
        if self is Piece.GIRAFFE:
            return (
                dir is Direction.FORWARD
                or dir is Direction.HORIZONTAL
                or dir is Direction.BACKWARD
            )
        if self is Piece.ELEPHANT:
            return dir is Direction.FORWARD_CROSS or dir is Direction.BACKWARD_CROSS
        if self is Piece.CHICK:
            return dir is Direction.FORWARD
        if self is Piece.HEN:
            return (
                dir is Direction.FORWARD
                or dir is Direction.FORWARD_CROSS
                or dir is Direction.HORIZONTAL
                or dir is Direction.BACKWARD
            )


def _square_repr(square: tuple[bool, Piece] | None) -> str:
    if not square:
        return "."
    if square[0]:
        match square[1]:
            case Piece.LION:
                return "l"
            case Piece.GIRAFFE:
                return "g"
            case Piece.ELEPHANT:
                return "e"
            case Piece.CHICK:
                return "c"
            case Piece.HEN:
                return "h"
    else:
        match square[1]:
            case Piece.LION:
                return "L"
            case Piece.GIRAFFE:
                return "G"
            case Piece.ELEPHANT:
                return "E"
            case Piece.CHICK:
                return "C"
            case Piece.HEN:
                return "H"


def _make_direction(horizontal_delta, vertical_delta) -> Direction | None:
    if horizontal_delta < 0:
        horizontal_delta = -horizontal_delta
    if vertical_delta == -1:
        if horizontal_delta == 0:
            return Direction.FORWARD
        if horizontal_delta == 1:
            return Direction.FORWARD_CROSS
    if vertical_delta == 0 and horizontal_delta == 1:
        return Direction.HORIZONTAL
    if vertical_delta == 1:
        if horizontal_delta == 0:
            return Direction.BACKWARD
        if horizontal_delta == 1:
            return Direction.BACKWARD_CROSS

    return None


class Game:
    """A class of animalshougi game."""

    turn: int
    hands: tuple[dict[Piece, int], dict[Piece, int]]
    table: list[list[tuple[bool, Piece] | None]]

    def __init__(self, *args):
        argc = len(args)
        if argc == 0:
            self.turn = 0
            empty_hands = {
                Piece.LION: 0,
                Piece.GIRAFFE: 0,
                Piece.ELEPHANT: 0,
                Piece.CHICK: 0,
            }
            self.hands = (empty_hands, empty_hands.copy())
            self.table = [
                [(True, Piece.GIRAFFE), (True, Piece.LION), (True, Piece.ELEPHANT)],
                [None, (True, Piece.CHICK), None],
                [None, (False, Piece.CHICK), None],
                [(False, Piece.ELEPHANT), (False, Piece.LION), (False, Piece.GIRAFFE)],
            ]
        elif argc == 1:
            serial_lines = args[0].split("\n")
            self.turn = int(serial_lines[0])
            self.hands = (
                {
                    Piece.LION: 1,
                    Piece.GIRAFFE: int(serial_lines[1][0]),
                    Piece.ELEPHANT: int(serial_lines[1][1]),
                    Piece.CHICK: int(serial_lines[1][2]),
                },
                {
                    Piece.LION: 1,
                    Piece.GIRAFFE: int(serial_lines[1][3]),
                    Piece.ELEPHANT: int(serial_lines[1][4]),
                    Piece.CHICK: int(serial_lines[1][5]),
                },
            )
            self.table = [[], [], [], []]
            for rank_id in range(4):
                for file_id in range(3):
                    ch = serial_lines[2 + rank_id][file_id]
                    if ch == "L":
                        self.hands[True][Piece.LION] = 0
                    if ch == "l":
                        self.hands[False][Piece.LION] = 0
                    self.table[rank_id].append(
                        (False, Piece.LION)
                        if ch == "L"
                        else (False, Piece.GIRAFFE)
                        if ch == "G"
                        else (False, Piece.ELEPHANT)
                        if ch == "E"
                        else (False, Piece.CHICK)
                        if ch == "C"
                        else (False, Piece.HEN)
                        if ch == "H"
                        else (True, Piece.LION)
                        if ch == "l"
                        else (True, Piece.GIRAFFE)
                        if ch == "g"
                        else (True, Piece.ELEPHANT)
                        if ch == "e"
                        else (True, Piece.CHICK)
                        if ch == "c"
                        else (True, Piece.HEN)
                        if ch == "h"
                        else None
                    )
        else:
            raise TypeError(
                f"Game.__init__() takes 1 or 2 positional arguments but {argc} were given"
            )

    def __eq__(self, other) -> bool:
        if type(self) is not Game:
            raise TypeError(
                f"descriptor '__eq__' requires a 'Game' object but received a '{type(self).__name__}'"
            )
        if type(other) is not Game:
            return NotImplemented
        return (
            self.turn == other.turn
            and self.hands == other.hands
            and self.table == other.table
        )

    def __repr__(self) -> str:
        return f"""{self.turn}
{self.hands[False][Piece.GIRAFFE]}{self.hands[False][Piece.ELEPHANT]}{self.hands[False][Piece.CHICK]}{self.hands[True][Piece.GIRAFFE]}{self.hands[True][Piece.ELEPHANT]}{self.hands[True][Piece.CHICK]}
{_square_repr(self.table[0][0])}{_square_repr(self.table[0][1])}{_square_repr(self.table[0][2])}
{_square_repr(self.table[1][0])}{_square_repr(self.table[1][1])}{_square_repr(self.table[1][2])}
{_square_repr(self.table[2][0])}{_square_repr(self.table[2][1])}{_square_repr(self.table[2][2])}
{_square_repr(self.table[3][0])}{_square_repr(self.table[3][1])}{_square_repr(self.table[3][2])}"""

    def can_move(self, src: tuple[int, int], dst: tuple[int, int]) -> bool:
        """Returns whether the piece can move from `src` to `dir` or not."""

        source_square = self.table[src[1]][src[0]]
        destination_square = self.table[dst[1]][dst[0]]

        if type(source_square) is not tuple:
            return False
        if (
            type(destination_square) is tuple
            and source_square[0] == destination_square[0]
        ):
            return False
        return source_square[1].can_move_toward(
            _make_direction(
                dst[0] - src[0],
                src[1] - dst[1] if source_square[0] else dst[1] - src[1],
            )
        )

    def _is_attacking(self, attacker: bool, coord: tuple[int, int]) -> bool:
        for rank_id in (
            range(0, 2)
            if coord[1] == 0
            else range(2, 4)
            if coord[1] == 3
            else range(coord[1] - 1, coord[1] + 2)
        ):
            for file_id in (
                range(0, 2)
                if coord[0] == 0
                else range(1, 3)
                if coord[0] == 2
                else range(0, 3)
            ):
                square = self.table[rank_id][file_id]
                if (
                    type(square) is tuple
                    and square[0] == attacker
                    and square[1].can_move_toward(
                        _make_direction(file_id - coord[0], rank_id - coord[1])
                        if attacker
                        else _make_direction(coord[0] - file_id, coord[1] - rank_id)
                    )
                ):
                    return True
        return False

    def winner(self) -> bool | None:
        if self.hands[False][Piece.LION]:
            return False
        if self.hands[True][Piece.LION]:
            return True
        f_lion = None
        t_lion = None
        for file_id in range(3):
            if self.table[0][file_id] == (False, Piece.LION):
                return self._is_attacking(True, (file_id, 0))
        for file_id in range(3):
            if self.table[3][file_id] == (True, Piece.LION):
                return not self._is_attacking(False, (file_id, 3))
        return None

    def move(self, src: tuple[int, int], dst: tuple[int, int]):
        """Moves the piece at `src` to `dst` if possible. otherwise, operates nothing and raises an error."""
        source_square = self.table[src[1]][src[0]]
        destination_square = self.table[dst[1]][dst[0]]

        player = bool(self.turn % 2)
        if self.winner() is not None:
            raise ValueError("The game has already finished")
        if not source_square:
            raise ValueError(f"No piece at {src}")
        if player != source_square[0]:
            raise ValueError(f"Cannot move piece of player {source_square[0]}")
        if not self.can_move(src, dst):
            raise ValueError(
                f"Cannot move piece {source_square} from {src} {dst} {destination_square}"
            )
        if destination_square:
            piece = destination_square[1]
            self.hands[player][piece if piece != Piece.HEN else Piece.CHICK] += 1
        self.table[dst[1]][dst[0]] = (
            (player, Piece.HEN)
            if source_square[1] == Piece.CHICK and (dst[1] == 0 or dst[1] == 3)
            else source_square
        )
        self.table[src[1]][src[0]] = None
        self.turn += 1

    def drop(self, hand: Piece, dst: tuple[int, int]):
        """Drops the `Piece` `hand` on `dst` if possible. otherwise, operates nothing and raises an error."""

        player = bool(self.turn % 2)
        if self.winner() is not None:
            raise ValueError("The game has already finished")

        if hand is Piece.HEN or self.hands[player][hand] <= 0:
            raise ValueError(f"The player {player} has no piece {hand}")
        if self.table[dst[1]][dst[0]]:
            raise ValueError(f"A piece already exists at {dst}")
        self.table[dst[1]][dst[0]] = (player, hand)
        self.hands[player][hand] -= 1
        self.turn += 1

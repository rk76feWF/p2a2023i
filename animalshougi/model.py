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

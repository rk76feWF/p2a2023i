import enum


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

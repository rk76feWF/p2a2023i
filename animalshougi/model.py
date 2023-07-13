import enum
@enum.unique
class Piece(enum.Enum):
    """An enum of piece animal."""

    LION = enum.auto()
    GIRAFFE = enum.auto()
    ELEPHANT = enum.auto()
    CHICK = enum.auto()
    HEN = enum.auto()

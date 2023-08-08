from animalshougi.model import Piece, Direction


def test_piece():
    pieces = [Piece.LION, Piece.GIRAFFE, Piece.ELEPHANT, Piece.CHICK, Piece.HEN]

    for piece in pieces:
        assert type(piece) == Piece

    for i in range(len(pieces)):
        for j in range(len(pieces)):
            assert (i == j) == (pieces[i] == pieces[j])


def test_can_move_toward():
    assert Piece.LION.can_move_toward(Direction.FORWARD_CROSS)
    assert Piece.LION.can_move_toward(Direction.FORWARD)
    assert Piece.LION.can_move_toward(Direction.HORIZONTAL)
    assert Piece.LION.can_move_toward(Direction.BACKWARD_CROSS)
    assert Piece.LION.can_move_toward(Direction.BACKWARD)

    assert Piece.ELEPHANT.can_move_toward(Direction.FORWARD_CROSS)
    assert Piece.ELEPHANT.can_move_toward(Direction.BACKWARD_CROSS)
    assert not Piece.ELEPHANT.can_move_toward(Direction.FORWARD)
    assert not Piece.ELEPHANT.can_move_toward(Direction.HORIZONTAL)
    assert not Piece.ELEPHANT.can_move_toward(Direction.BACKWARD)

    assert Piece.GIRAFFE.can_move_toward(Direction.FORWARD)
    assert Piece.GIRAFFE.can_move_toward(Direction.HORIZONTAL)
    assert Piece.GIRAFFE.can_move_toward(Direction.BACKWARD)
    assert not Piece.GIRAFFE.can_move_toward(Direction.FORWARD_CROSS)
    assert not Piece.GIRAFFE.can_move_toward(Direction.BACKWARD_CROSS)

    assert Piece.HEN.can_move_toward(Direction.FORWARD_CROSS)
    assert Piece.HEN.can_move_toward(Direction.FORWARD)
    assert Piece.HEN.can_move_toward(Direction.HORIZONTAL)
    assert Piece.HEN.can_move_toward(Direction.BACKWARD)
    assert not Piece.HEN.can_move_toward(Direction.BACKWARD_CROSS)

    assert Piece.CHICK.can_move_toward(Direction.FORWARD)
    assert not Piece.CHICK.can_move_toward(Direction.FORWARD_CROSS)
    assert not Piece.CHICK.can_move_toward(Direction.HORIZONTAL)
    assert not Piece.CHICK.can_move_toward(Direction.BACKWARD_CROSS)
    assert not Piece.CHICK.can_move_toward(Direction.BACKWARD)

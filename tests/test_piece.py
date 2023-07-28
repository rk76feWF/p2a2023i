from animalshougi.model import Piece


def test_piece():
    pieces = [Piece.LION, Piece.GIRAFFE, Piece.ELEPHANT, Piece.CHICK, Piece.HEN]

    for piece in pieces:
        assert type(piece) == Piece

    for i in range(len(pieces)):
        for j in range(len(pieces)):
            assert (i == j) == (pieces[i] == pieces[j])

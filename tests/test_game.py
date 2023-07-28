from animalshougi.model import Game, Piece
import pytest


def test_init():
    g = Game()

    assert g.turn == 0
    empty_hands = {
        Piece.LION: 0,
        Piece.GIRAFFE: 0,
        Piece.ELEPHANT: 0,
        Piece.CHICK: 0,
    }
    assert g.hands == (empty_hands, empty_hands)
    assert g.table == [
        [(True, Piece.GIRAFFE), (True, Piece.LION), (True, Piece.ELEPHANT)],
        [None, (True, Piece.CHICK), None],
        [None, (False, Piece.CHICK), None],
        [(False, Piece.ELEPHANT), (False, Piece.LION), (False, Piece.GIRAFFE)],
    ]

    g = Game(f"1\n001000\ngle\n.C.\n...\nELG")

    assert g.turn == 1
    having_chick = empty_hands.copy()
    having_chick[Piece.CHICK] = 1
    assert g.hands == (having_chick, empty_hands)
    assert g.table == [
        [(True, Piece.GIRAFFE), (True, Piece.LION), (True, Piece.ELEPHANT)],
        [None, (True, Piece.CHICK), None],
        [None, None, None],
        [(False, Piece.ELEPHANT), (False, Piece.LION), (False, Piece.GIRAFFE)],
    ]

    having_lion = empty_hands.copy()
    having_lion[Piece.LION] = 1

    g = Game(f"65537\n000000\ng.e\n.c.\n.C.\nELG")

    assert g.turn == 65537
    assert g.hands == (having_lion, empty_hands)
    assert g.table == [
        [(True, Piece.GIRAFFE), None, (True, Piece.ELEPHANT)],
        [None, (True, Piece.CHICK), None],
        [None, (False, Piece.CHICK), None],
        [(False, Piece.ELEPHANT), (False, Piece.LION), (False, Piece.GIRAFFE)],
    ]
    g = Game(f"65537\n000000\ngle\n.c.\n.C.\nE.G")

    assert g.turn == 65537
    assert g.hands == (empty_hands, having_lion)
    assert g.table == [
        [(True, Piece.GIRAFFE), (True, Piece.LION), (True, Piece.ELEPHANT)],
        [None, (True, Piece.CHICK), None],
        [None, (False, Piece.CHICK), None],
        [(False, Piece.ELEPHANT), None, (False, Piece.GIRAFFE)],
    ]

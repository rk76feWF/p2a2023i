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
        [(False, Piece.GIRAFFE), (False, Piece.LION), (False, Piece.ELEPHANT)],
        [None, (True, Piece.CHICK), None],
        [None, (False, Piece.CHICK), None],
        [(True, Piece.ELEPHANT), (True, Piece.LION), (True, Piece.GIRAFFE)],
    ]

    g = Game(f"1\n001000\ngle\n.C.\n...\nELG")

    assert g.turn == 1
    having_chick = empty_hands.copy()
    having_chick[Piece.CHICK] = 1
    assert g.hands == (having_chick, empty_hands)
    assert g.table == [
        [(False, Piece.GIRAFFE), (False, Piece.LION), (False, Piece.ELEPHANT)],
        [None, (False, Piece.CHICK), None],
        [None, None, None],
        [(True, Piece.ELEPHANT), (True, Piece.LION), (True, Piece.GIRAFFE)],
    ]

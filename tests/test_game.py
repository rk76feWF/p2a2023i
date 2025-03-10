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
        [None, (False, Piece.CHICK), None],
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


def test_game_repr():
    game = Game()  # サンプルのGameオブジェクトを作成
    serialized = game.__repr__()  # Gameオブジェクトの__repr__メソッドを呼び出し、シリアライズされた文字列を取得

    # 期待されるシリアライズ結果と比較してテストする
    expected = "0\n000000\ngle\n.c.\n.C.\nELG"

    assert serialized == expected
    assert (
        repr(Game("0\n000000\ngle\n.c.\n.C.\nELG")) == "0\n000000\ngle\n.c.\n.C.\nELG"
    )
    assert (
        repr(Game("1\n001000\ngle\n.C.\n...\nELG")) == "1\n001000\ngle\n.C.\n...\nELG"
    )  # 先手が持ち駒を得る
    assert (
        repr(Game("2\n001001\ng.e\n.l.\n...\nELG")) == "2\n001001\ng.e\n.l.\n...\nELG"
    )  # 後手が持ち駒を得る
    assert (
        repr(Game("3\n001001\ng.e\n.l.\n.E.\n.LG")) == "3\n001001\ng.e\n.l.\n.E.\n.LG"
    )
    assert (
        repr(Game("4\n001000\ng.e\n.lc\n.E.\n.LG")) == "4\n001000\ng.e\n.lc\n.E.\n.LG"
    )
    assert (
        repr(Game("9\n100000\n..e\nClc\n.E.\n.LG")) == "9\n100000\n..e\nClc\n.E.\n.LG"
    )
    assert (
        repr(Game("11\n100000\nH.e\n.lc\n.E.\n.LG")) == "11\n100000\nH.e\n.lc\n.E.\n.LG"
    )  # 鶏になる
    assert (
        repr(Game("12\n000000\nH.e\n.lc\n.E.\nhLG")) == "12\n000000\nH.e\n.lc\n.E.\nhLG"
    )  # 鶏になる


def test_eq():
    g = Game()
    assert g == Game()
    assert g == Game("0\n000000\ngle\n.c.\n.C.\nELG")

    sample = lambda x: Game(x) == Game(x)

    assert sample("0\n000000\ngle\n.c.\n.C.\nELG")
    assert sample("1\n001000\ngle\n.C.\n...\nELG")
    assert sample("2\n001001\ng.e\n.l.\n...\nELG")
    assert sample("3\n001001\ng.e\n.l.\n.E.\n.LG")
    assert sample("4\n001000\ng.e\n.lc\n.E.\n.LG")
    assert sample("9\n100000\n..e\nClc\n.E.\n.LG")
    assert sample("11\n100000\nH.e\n.lc\n.E.\n.LG")
    assert sample("12\n000000\nH.e\n.lc\n.E.\nhLG")

    assert g != Game("1\n001000\ngle\n.C.\n...\nELG")

    class ALL_EQ:
        def __eq__(*_):
            return True

    assert g == ALL_EQ()
    assert ALL_EQ() == g

    class ALL_NE:
        def __eq__(*_):
            return False

    assert g != ALL_NE()
    assert ALL_NE() != g


def test_can_move():
    g = Game()
    assert not g.can_move((0, 3), (1, 3))
    assert not g.can_move((0, 3), (1, 2))
    assert not g.can_move((0, 3), (2, 1))

    assert g.can_move((1, 3), (0, 2))
    assert not g.can_move((1, 3), (1, 2))
    assert g.can_move((1, 3), (2, 2))

    assert g.can_move((2, 3), (2, 2))
    assert not g.can_move((2, 3), (1, 3))
    assert g.can_move((1, 2), (1, 1))

    assert g.can_move((1, 1), (1, 2))

    assert g.can_move((0, 0), (0, 1))

    assert not g.can_move((0, 2), (0, 1))


def test_winner():
    g = Game()
    assert g.winner() is None

    assert Game("0\n000000\ng.e\n.c.\n.C.\nELG").winner() == False

    assert Game("0\n000000\ngle\n.c.\n.C.\nE.G").winner() == True

    assert Game("0\n000000\ng.L\nlc.\n.C.\nE.G").winner() == False
    assert Game("0\n000000\n.gL\nlc.\n.C.\nE.G").winner() == True

    assert Game("0\n000000\ng.e\n.c.\n.CL\nl.G").winner() == True
    assert Game("0\n000000\ng.e\n.c.\n.CL\nlG.").winner() == False


def test_move():
    g = Game()
    g.move((1, 2), (1, 1))
    assert g == Game("1\n001000\ngle\n.C.\n...\nELG")

    with pytest.raises(ValueError):
        g.move((1, 3), (1, 2))
    assert g == Game("1\n001000\ngle\n.C.\n...\nELG")

    g.move((1, 0), (0, 1))
    assert g == Game("2\n001000\ng.e\nlC.\n...\nELG")

    with pytest.raises(ValueError):
        g.move((0, 3), (0, 2))
    assert g == Game("2\n001000\ng.e\nlC.\n...\nELG")

    g.move((1, 1), (1, 0))
    assert g == Game("3\n001000\ngHe\nl..\n...\nELG")

    g.move((0, 1), (0, 2))
    assert g == Game("4\n001000\ngHe\n...\nl..\nELG")

    g.move((1, 3), (2, 2))
    assert g == Game("5\n001000\ngHe\n...\nl.L\nE.G")

    g.move((0, 2), (0, 3))
    assert g == Game("6\n001010\ngHe\n...\n..L\nl.G")
    assert g.winner() == True

    with pytest.raises(ValueError):
        g.move((2, 3), (1, 3))
    assert g == Game("6\n001010\ngHe\n...\n..L\nl.G")

    g = Game("1\n000000\n.l.\n...\n.c.\n.L.")
    g.move((1, 2), (1, 3))
    assert g == Game("2\n000000\n.l.\n...\n...\n.h.")
    assert g.winner() == True

    with pytest.raises(ValueError):
        Game("1\n000000\ng.e\n.c.\n.C.\nELG").move((0, 0), (0, 1))


def test_drop():
    g = Game("4\n001001\n.ge\nl..\n...\nELG")
    g.drop(Piece.CHICK, (0, 0))
    assert g == Game("5\n000001\nCge\nl..\n...\nELG")

    with pytest.raises(ValueError):
        g.drop(Piece.GIRAFFE, (1, 2))
    assert g == Game("5\n000001\nCge\nl..\n...\nELG")

    with pytest.raises(ValueError):
        g.drop(Piece.CHICK, (1, 3))
    assert g == Game("5\n000001\nCge\nl..\n...\nELG")

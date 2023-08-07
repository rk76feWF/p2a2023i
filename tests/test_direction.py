from animalshougi.model import Direction


def test_direction():
    dirs = [
        Direction.FORWARD,
        Direction.FORWARD_CROSS,
        Direction.HORIZONTAL,
        Direction.BACKWARD_CROSS,
        Direction.BACKWARD,
    ]

    for d in dirs:
        assert type(d) is Direction

    for i in range(len(dirs)):
        for j in range(len(dirs)):
            assert (i == j) == (dirs[i] == dirs[j])

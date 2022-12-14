from anya import anya
from grid import Map


def test_1():
    map_ = Map()
    map_.read_from_string("....\n..#.\n.##.\n....", 4, 4)
    dist, path = anya(map_, (3, 1), (1, 3))
    assert dist == 3.414213562373095


def test_2():
    map_str = "..#.\n##.#\n#..#\n...#"
    map_ = Map()
    map_.read_from_string(map_str, 4, 4)
    length, path = anya(map_, (0, 4), (2, 2))
    assert length == -1


def test_3():
    map_str = "...#\n....\n##..\n#..#"
    map_ = Map()
    map_.read_from_string(map_str, 4, 4)
    length, path = anya(map_, (3, 0), (2, 0))
    assert length == -1


def test_4():
    map_ = Map()
    map_.read_from_string("#.#.\n....\n###.\n#...", 4, 4)
    length, path = anya(map_, (0, 0), (0, 1))
    assert length == -1


def test_5():
    map_ = Map()
    map_.read_from_string("..#.\n#...\n...#\n.#..", 4, 4)
    length, path = anya(map_, (0, 0), (4, 0))
    assert length == -1


def test_6():
    map_ = Map()
    map_.read_from_string("..#.\n#.#.\n..#.\n#.#.", 4, 4)
    length, path = anya(map_, (3, 2), (2, 3))
    assert length == -1


def test_7():
    map_ = Map()
    map_.read_from_string("#.##\n#..#\n.#..\n#.#.", 4, 4)
    length, path = anya(map_, (0, 1), (0, 3))
    assert length == -1


def test_8():
    map_ = Map()
    map_.read_from_string("###.\n#.##\n#.#.\n####", 4, 4)
    length, path = anya(map_, (2, 1), (2, 3))
    assert length == -1

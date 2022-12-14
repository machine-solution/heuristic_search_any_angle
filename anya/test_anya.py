from anya import anya
from grid import Map


def test_1():
    map_ = Map()
    map_.read_from_string("....\n..#.\n.##.\n....", 4, 4)
    dist, path = anya(map_, (3, 1), (1, 3))
    assert dist == 3.414213562373095


def test_2():
    map_ = Map()
    map_.read_from_string("....\n..#.\n.##.\n....", 4, 4)
    length, path = anya(map_, (3, 1), (1, 3))
    assert length == 3.414213562373095

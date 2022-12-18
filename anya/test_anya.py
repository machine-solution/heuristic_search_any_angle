import unittest

from .anya import anya
from .grid import Map


class Tests(unittest.TestCase):

    def test_1(self):
        map_ = Map()
        map_.read_from_string("....\n..#.\n.##.\n....", 4, 4)
        dist, path = anya(map_, (3, 1), (1, 3), 1)
        self.assertEqual(dist, 3.414213562373095)

    def test_2(self):
        map_str = "..#.\n##.#\n#..#\n...#"
        map_ = Map()
        map_.read_from_string(map_str, 4, 4)
        length, path = anya(map_, (0, 4), (2, 2), 1)
        self.assertEqual(length, -1)

    def test_3(self):
        map_str = "...#\n....\n##..\n#..#"
        map_ = Map()
        map_.read_from_string(map_str, 4, 4)
        length, path = anya(map_, (3, 0), (2, 0), 1)
        self.assertEqual(length, -1)

    def test_4(self):
        map_ = Map()
        map_.read_from_string("#.#.\n....\n###.\n#...", 4, 4)
        length, path = anya(map_, (0, 0), (0, 1), 1)
        self.assertEqual(length, -1)

    def test_5(self):
        map_ = Map()
        map_.read_from_string("..#.\n#...\n...#\n.#..", 4, 4)
        length, path = anya(map_, (0, 0), (4, 0), 1)
        self.assertEqual(length, 4.650281539872885)

    def test_6(self):
        map_ = Map()
        map_.read_from_string("..#.\n#.#.\n..#.\n#.#.", 4, 4)
        length, path = anya(map_, (3, 2), (2, 3), 1)
        self.assertEqual(length, -1)

    def test_7(self):
        map_ = Map()
        map_.read_from_string("#.##\n#..#\n.#..\n#.#.", 4, 4)
        length, path = anya(map_, (0, 1), (0, 3), 1)
        self.assertEqual(length, -1)

    def test_8(self):
        map_ = Map()
        map_.read_from_string("###.\n#.##\n#.#.\n####", 4, 4)
        length, path = anya(map_, (2, 1), (2, 3), 1)
        self.assertEqual(length, -1)

    def test_9(self):
        map_ = Map()
        map_.read_from_string(".###\n..#.\n.##.\n....", 4, 4)
        length, path = anya(map_, (2, 2), (0, 2), 1)
        self.assertEqual(length, -1)

    def test_10(self):
        map_ = Map()
        map_.read_from_string(".@@@\n.@@.\n....\n....", 4, 4)
        length, path = anya(map_, (2, 2), (2, 2), 1)
        self.assertEqual(length, 0)

    def test_11(self):
        map_ = Map()
        map_.read_from_string('.@..\n...@\n.@@@\n...@', 4, 4)
        length, path = anya(map_, (4, 0), (0, 2), 1)
        self.assertEqual(length, 4.650281539872885)

    def test_12(self):
        map_ = Map()
        map_.read_from_string('@...\n...@\n....\n...@', 4, 4)
        length, path = anya(map_, (0, 3), (3, 2), 1)
        self.assertEqual(length, 3.1622776601683795)

    def test_13(self):
        map_ = Map()
        map_.read_from_string('@...\n....\n@.@.\n@..@', 4, 4)
        length, path = anya(map_, (0, 2), (4, 3), 1)
        self.assertEqual(length, 4.414213562373095)

    def test_14(self):
        map_ = Map()
        map_.read_from_string('@...\n@...\n@@..\n@@@@', 4, 4)
        length, path = anya(map_, (3, 4), (0, 2), 1)
        self.assertEqual(length, 3.605551275463989)

    def test_15(self):
        map_ = Map()
        map_.read_from_string('...@\n...@\n..@.\n.@.@', 4, 4)
        length, path = anya(map_, (3, 0), (1, 4), 1)
        self.assertEqual(length, -1)

    def test_16(self):
        map_ = Map()
        map_.read_from_string('@...\n..@.\n@...\n....', 4, 4)
        length, path = anya(map_, (3, 2), (0, 0), 1)
        self.assertEqual(length, -1)

    def test_17(self):
        map_ = Map()
        map_.read_from_string('@.@.\n.@@.\n@@.@\n....', 4, 4)
        length, path = anya(map_, (4, 0), (2, 3), 1)
        self.assertEqual(length, 3.6502815398728847)

    def test_18(self):
        map_ = Map()
        map_.read_from_string('.@..\n....\n..@@\n@@@@', 4, 4)
        length, path = anya(map_, (2, 3), (0, 0), 1)
        self.assertEqual(length, 3.6502815398728847)

import typing as tp

from ..common.api import Stats, Algorithm, M


class TestCase:
    def __init__(self, difficulty, start, goal, optimal):
        self.difficulty = difficulty
        self.start = start
        self.goal = goal
        self.optimal = optimal


class TestSet(tp.Generic[M]):
    def __init__(self, name, path, output, algo: Algorithm[M]):
        self.algo = algo
        self.tests: tp.List[TestCase] = []
        self.max_diff = 0
        self.name = name

        self.read_from_file(path)
        self.input_path = path
        self.output_path = output

    def read_from_file(self, path):
        map_data = read_map_from_file(path + ".map")
        self.map = self.algo.read_map(*map_data)
        self.tests = read_scenes_from_file(path + ".map.scen")
        self.max_diff = max([item.difficulty for item in self.tests])

    def choose_tests(self, number):
        tests = []
        i = 0
        for diff in range(number):
            target = diff * self.max_diff // number
            while self.tests[i].difficulty != target:
                i += 1
            tests.append(self.tests[i])
            i += 1
        return tests


"""
class SearchCase:
    def __init__(self, f_i, h_i, w_i, k_i):
        self.f_i = f_i
        self.h_i = h_i
        self.w_i = w_i
        self.k_i = k_i

    def __str__(self):
        return fnames[self.f_i] + "." + hnames[self.h_i] + ".w=" + str(ws[self.w_i]) + "_k=" + str(ks[self.k_i])s
"""


def compute_stats(stats: Stats, node, optimal) -> Stats:
    if node is not None:
        stats.suboptimal = round(stats.way_length / optimal, 6)
        stats.runtime = round(stats.runtime, 6)
    return stats


def read_map_from_file(path) -> tp.Tuple[str, int, int]:
    with open(path, "r") as f:
        map_type = f.readline()
        height = f.readline().split()[1]
        width = f.readline().split()[1]
        f.readline()
        # now we read the map
        map_canvas = "\n".join(f.readlines())
        return map_canvas, int(width), int(height)


def read_scenes_from_file(path) -> tp.List[TestCase]:
    tests = []
    with open(path, "r") as f:
        version = f.readline()
        for data in f.readlines():
            difficulty, _,_,_, start_y, start_x, goal_y, goal_x, optimal = data.split()
            test = TestCase(int(difficulty), (int(start_x), int(start_y)), (int(goal_x), int(goal_y)), float(optimal))
            tests.append(test)
    return tests



import typing as tp
from fractions import Fraction
from math import ceil, floor

from grid import Map


Number = tp.Union[int, Fraction]


def euclidean_distance(s: tp.Tuple[Number, Number], t: tp.Tuple[Number, Number]) -> float:
    return ((s[0]-t[0])**2 + (s[1]-t[1])**2) ** 0.5


def split_interval_at_corner_points(grid: Map, interval: tp.Tuple[Fraction, Fraction, int]) -> \
        tp.List[tp.Tuple[Fraction, Fraction, int]]:

    intervals = []
    l, r, row = interval
    cur = l
    for i in range(ceil(l), floor(r + 1)):
        if grid.is_corner_point(row, i) and cur != i:
            intervals.append((cur, Fraction(i), row))
            cur = Fraction(i)
    if cur != r or len(intervals) == 0:
        intervals.append((cur, r, row))
    return intervals


class Stats:
    def __init__(self):
        self.difficulty = 0
        self.expansions = 0 # algorithm must set this value
        self.runtime = 0 # algorithm must set this value
        self.way_length = 0 # algorithm must set this value
        self.suboptimal = 0
        self.max_tree_size = 0 # algorithm must set this value

    def read_from_string(self, data):
        delimiter = ","
        diff, expansions, runtime, way_length, suboptimal, tree_size = data.split(delimiter)
        self.difficulty = int(diff)
        self.expansions = int(expansions)
        self.runtime = float(runtime)
        self.way_length = float(way_length)
        self.suboptimal = int(suboptimal)
        self.max_tree_size = int(tree_size)
        
        
    def __repr__(self):
        delimiter = ","
        return str(self.difficulty) + delimiter + str(self.expansions) + delimiter + str(self.runtime) + delimiter + str(self.way_length) +\
        delimiter + str(self.suboptimal)  + delimiter + str(self.max_tree_size)
    
    def header(self):
        delimiter = ","
        return "difficulty" + delimiter + "expansions" + delimiter + "runtime" + delimiter + "way_length" +\
        delimiter + "suboptimal" + delimiter + "max_tree_size"

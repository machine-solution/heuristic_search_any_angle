import typing as tp
from abc import ABC, abstractmethod

from .grid import Map


M = tp.TypeVar('M', bound=Map)


class Algorithm(ABC, tp.Generic[M]):
    @staticmethod
    @abstractmethod
    def read_map(cell_str: str, width: int, height: int) -> M:
        pass

    @staticmethod
    @abstractmethod
    def compute_path(map_: M) -> "Stats":
        pass


class Stats:
    def __init__(self):
        self.difficulty = 0
        self.expansions = 0  # algorithm must set this value
        self.runtime = 0  # algorithm must set this value
        self.way_length = 0  # algorithm must set this value
        self.suboptimal = 0
        self.max_tree_size = 0  # algorithm must set this value

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
        return str(self.difficulty) + delimiter + str(self.expansions) + delimiter + str(self.runtime) + \
               delimiter + str(self.way_length) + delimiter + str(self.suboptimal) + delimiter + str(self.max_tree_size)

    def header(self):
        delimiter = ","
        return "difficulty" + delimiter + "expansions" + delimiter + "runtime" + delimiter + \
               "way_length" + delimiter + "suboptimal" + delimiter + "max_tree_size"

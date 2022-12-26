import typing as tp
from abc import ABC

from ..common.api import Algorithm, Stats
from .grid import MapTheta
from .theta_ap import theta_ap
from .lazy_theta import lazy_theta
from .utils import euclidian_distance, weighted_heuristic
from .search_tree import SearchTreePQS


class Theta(Algorithm[MapTheta], ABC):
    @staticmethod
    def read_map(cell_str: str, width: int, height: int) -> MapTheta:
        map_ = MapTheta()
        map_.read_from_string(cell_str, width, height)
        return map_


class ThetaAPWithEuclideanHeuristics(Theta):
    @staticmethod
    def compute_path_from_map(map_: MapTheta, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
        return theta_ap(map_, *start, *end, euclidian_distance, SearchTreePQS)[2]


class ThetaAPWithWeightedHeuristics(Theta):
    @staticmethod
    def compute_path_from_map(map_: MapTheta, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
        return theta_ap(map_, *start, *end, weighted_heuristic, SearchTreePQS)[2]


class LazyThetaWithEuclideanHeuristics(Theta):
    @staticmethod
    def compute_path_from_map(map_: MapTheta, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
        return lazy_theta(map_, *start, *end, euclidian_distance, SearchTreePQS)[2]


class LazyThetaWithWeightedHeuristics(Theta):
    @staticmethod
    def compute_path_from_map(map_: MapTheta, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
        return lazy_theta(map_, *start, *end, weighted_heuristic, SearchTreePQS)[2]

import typing as tp
from abc import ABC

from ..common.api import Algorithm, Stats
from ._2k_astar import Map2K, canonical_astar, astar
from .utils import euclidian_distance, h_2k, SearchTreePQS


class AStarAlgo(Algorithm[Map2K], ABC):
    @staticmethod
    def read_map(cell_str: str, width: int, height: int) -> Map2K:
        map_ = Map2K()
        map_.read_from_string(cell_str, width, height)
        return map_


def create_canonical_algo_with_euclidean_heuristics(k, w=1) -> Algorithm:

    assert k >= 3, "k should be >= 3"

    class Inner(AStarAlgo):
        @staticmethod
        def compute_path_from_map(map_: Map2K, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
            return canonical_astar(map_, start[0], start[1], end[0], end[1], euclidian_distance, SearchTreePQS, w, k)[2]

    return Inner()


def create_canonical_algo_with_h_2k_heuristics(k, w=1) -> Algorithm:

    assert k >= 3, "k should be >= 3"

    class Inner(AStarAlgo):
        @staticmethod
        def compute_path_from_map(map_: Map2K, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
            return canonical_astar(map_, start[0], start[1], end[0], end[1], h_2k, SearchTreePQS, w, k)[2]

    return Inner()


def create_2k_astar_algo_with_euclidean_heuristics(k, w=1) -> Algorithm:

    assert k >= 3, "k should be >= 3"

    class Inner(AStarAlgo):
        @staticmethod
        def compute_path_from_map(map_: Map2K, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
            return astar(map_, start[0], start[1], end[0], end[1], euclidian_distance, SearchTreePQS, w, k)[2]

    return Inner()


def create_2k_astar_algo_with_h_2k_heuristics(k, w=1) -> Algorithm:

    assert k >= 3, "k should be >= 3"

    class Inner(AStarAlgo):
        @staticmethod
        def compute_path_from_map(map_: Map2K, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
            return astar(map_, start[0], start[1], end[0], end[1], h_2k, SearchTreePQS, w, k)[2]

    return Inner()

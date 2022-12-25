import typing as tp

from ..common.api import Algorithm, Stats
from .full_graph_algorithm import MapFullGraph, full_graph_astar
from .._2k_astar.utils import euclidian_distance, SearchTreePQS


class FullGraph(Algorithm[MapFullGraph]):
    @staticmethod
    def read_map(cell_str: str, width: int, height: int) -> MapFullGraph:
        map_ = MapFullGraph()
        map_.read_from_string(cell_str, width, height)
        return map_

    @staticmethod
    def compute_path_from_map(map_: MapFullGraph, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
        return full_graph_astar(map_, *start, *end, euclidian_distance, SearchTreePQS)

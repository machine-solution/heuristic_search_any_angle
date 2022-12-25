import typing as tp

from ..common.api import Algorithm, Stats
from ..common.grid import Map
from .anya import anya


class Anya(Algorithm[Map]):
    @staticmethod
    def read_map(cell_str: str, width: int, height: int) -> Map:
        map_ = Map()
        map_.read_from_string(cell_str, width, height)
        return map_

    @staticmethod
    def compute_path_from_map(map_: Map, start: tp.Tuple[int, int], end: tp.Tuple[int, int]) -> Stats:
        _, _, res = anya(map_, start, end)
        if isinstance(res, Stats):
            return res

        print(res)
        assert False, "Not reachable"

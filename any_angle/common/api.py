import typing as tp
from abc import ABC, abstractmethod

from .grid import Map


M = tp.TypeVar('M', bound=Map)


class Algorithm(ABC, tp.Generic[M]):
    @staticmethod
    @abstractmethod
    def read_map(cell_str: str, width: int, height: int) -> M:
        pass

import typing as tp
from fractions import Fraction
from math import ceil, floor

from ..common.grid import Map


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

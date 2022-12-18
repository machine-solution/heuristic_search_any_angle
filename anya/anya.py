import typing as tp
from fractions import Fraction
from math import ceil, floor
from heapq import heapify, heappush, heappop
from collections import defaultdict
import time

from .grid import Map
from .utils import euclidean_distance, split_interval_at_corner_points, Stats


class Node:
    def __init__(self, interval: tp.Tuple[Fraction, Fraction], row: int, root: tp.Tuple[int, int],
                 g_value: float, f_value: float, is_start: bool = False):
        self.interval = interval
        self.row = row
        self.root = root
        self.g_value = g_value
        self.is_start = is_start
        self.f_value = f_value
        self.bounds: tp.Tuple[bool, bool] = (True, True)
        self.parent: tp.Optional["Node"] = None
        if self.root[0] == self.row and self.root[1] == self.interval[0]:
            self.bounds = (False, True)
        if self.root[0] == self.row and self.root[1] == self.interval[1]:
            self.bounds = (True, False)

    @property
    def is_flat_node(self):
        return self.row == self.root[0]

    def contains_point(self, point: tp.Tuple[int, int]) -> bool:
        left = (lambda x, y: x <= y) if self.bounds[0] else (lambda x, y: x < y)
        right = (lambda x, y: x <= y) if self.bounds[1] else (lambda x, y: x < y)
        return self.row == point[0] and left(self.interval[0], point[1]) and right(point[1], self.interval[1])

    def is_empty(self):
        return (self.interval[0] == self.interval[1] and (not self.bounds[0] or not self.bounds[1])) or \
               (self.interval[0] > self.interval[1])

    def __lt__(self, other):
        return self.f_value < other.f_value

    def __hash__(self):
        return hash((self.interval, self.row, self.root, self.g_value))

    def __eq__(self, other):
        return (self.interval, self.row, self.root, self.g_value) == \
               (other.interval, other.row, other.root, other.g_value)


def calculate_f_value(interval: tp.Tuple[Fraction, Fraction], row: int, root: tp.Tuple[int, int],
                      root_dist: float, target: tp.Tuple[int, int]) -> float:
    if (root[0] > row and target[0] > row) or (root[0] < row and target[0] < row):
        target = (2 * row - target[0], target[1])

    if root[0] < row <= target[0] or target[0] <= row < root[0]:
        intersection = root[1] + Fraction(target[1] - root[1], target[0] - root[0]) * (row - root[0])
        x: Fraction
        if interval[0] <= intersection <= interval[1]:
            x = intersection
        elif intersection > interval[1]:
            x = interval[1]
        else:
            x = interval[0]

        # print("cone f", interval, row, root)
        return root_dist + euclidean_distance(root, (row, x)) + euclidean_distance((row, x), target)
    elif root[0] == row:
        x = interval[0] if abs(interval[0] - root[1]) < abs(interval[1] - root[1]) else interval[1]
        # print("flat f", interval, row, root, root_dist, euclidean_distance(root, (row, x)),
        # euclidean_distance((row, x), target))
        return root_dist + euclidean_distance(root, (row, x)) + euclidean_distance((row, x), target)
    else:
        assert False, "Not reachable"


def generate_start_successors(grid: Map, s: tp.Tuple[int, int], target: tp.Tuple[int, int]) -> tp.List[Node]:
    if not grid.is_traversible(s[0], s[1]):
        return []

    # construct a maximal half-closed interval I1 containing all points observable and to the left of s
    l = s[1]
    while l >= 0 and grid.visible(s[0], s[1], s[0], l):
        l -= 1
    l += 1

    I1 = (l, s[1], s[0])  # (l, r, row)

    # construct a maximal half-closed interval I2 containing all points observable and to the right of s
    r = s[1]
    while r <= grid.width and grid.visible(s[0], s[1], s[0], r):
        r += 1
    r -= 1

    I2 = (s[1], r, s[0])  # (l, r, row)

    # construct a maximal closed interval I3 containing all points observable and from the row above s
    if s[0] < grid.height:
        l = 0
        while l < grid.width and not grid.visible(s[0], s[1], s[0] + 1, l):
            l += 1

        if not grid.visible(s[0], s[1], s[0] + 1, l):
            I3 = None
        else:
            r = l
            while r < grid.width and grid.visible(s[0], s[1], s[0] + 1, r):
                r += 1

            if not grid.visible(s[0], s[1], s[0] + 1, r):
                r -= 1

            I3 = (l, r, s[0] + 1)  # (l, r, row)
    else:
        I3 = None

    # construct a maximal closed interval I4 containing all points observable and from the row below s
    if s[0] > 0:
        l = 0
        while l < grid.width and not grid.visible(s[0], s[1], s[0] - 1, l):
            l += 1

        if not grid.visible(s[0], s[1], s[0] - 1, l):
            I4 = None
        else:
            r = l
            while r < grid.width and grid.visible(s[0], s[1], s[0] - 1, r):
                r += 1

            if not grid.visible(s[0], s[1], s[0] - 1, r):
                r -= 1

            I4 = (l, r, s[0] - 1)  # (l, r, row)
    else:
        I4 = None

    # Split each Ik at each corner point and take their unions
    intervals: tp.List[tp.Tuple[Fraction, Fraction, int]] = []
    for interval in [I1, I2, I3, I4]:
        if interval is None:
            continue
        l, r, row = interval
        intervals += split_interval_at_corner_points(grid, (Fraction(l), Fraction(r), row))

    # print("I1 I2 I3 I4", I1, I2, I3, I4)

    # construct successors
    result = []
    for (l_, r_, row) in intervals:
        # print("start succ", (l_, r_), row, s)
        result.append(Node((l_, r_), row, s, g_value=0, f_value=euclidean_distance(s, target)))

    return result


def generate_flat_successors(grid: Map, p: tp.Tuple[int, Fraction], r: tp.Tuple[int, int],
                             col_dir: tp.Literal[1, -1], r_dist: float, target: tp.Tuple[int, int]) -> tp.List[Node]:
    q_col: int
    if col_dir == 1:
        q_col = ceil(p[1])
    else:
        q_col = floor(p[1])

    while (q_col < grid.width or col_dir == -1) and (q_col > 0 or col_dir == 1) and \
            not grid.is_between_obstacles(p[0], q_col) and (q_col == p[1] or not grid.is_corner_point(p[0], q_col)) \
            and grid.is_traversable_edge(p[0], q_col, col_dir):
        q_col += col_dir

    interval = (min(Fraction(q_col), p[1]), max(Fraction(q_col), p[1]))
    if r[0] == p[0]:
        return [Node(interval, p[0], r, g_value=r_dist, f_value=calculate_f_value(interval, p[0], r, r_dist, target))]
    else:
        assert p[1].denominator == 1
        root = (p[0], p[1].numerator)
        root_dist = r_dist + euclidean_distance(r, p)
        return [Node(interval, p[0], root, g_value=root_dist,
                     f_value=calculate_f_value(interval, p[0], root, root_dist, target))]


def generate_non_observable_cone_successors(grid: Map, row: int, a: int, root: tp.Tuple[int, int],
                                            row_dir: tp.Literal[-1, 1], col_dir: tp.Literal[-1, 1],
                                            root_dist: float, target: tp.Tuple[int, int]) -> tp.List[Node]:
    I_max: tp.Tuple[Fraction, Fraction, int]  # (l, r, row)
    new_root: tp.Tuple[int, int] = (row, a)
    dist: float = euclidean_distance(root, (row, a))

    q: int
    if row == root[0]:
        # Non-observable successors of a flat node
        assert a.denominator == 1
        a = int(a)

        p: tp.Tuple[int, int] = (row + row_dir, a)
        q = p[1]

        if col_dir == 1 and row_dir == 1:
            while grid.get_cell(p[0] - 1, q) == 0:
                q += 1
        elif col_dir == 1 and row_dir == -1:
            while grid.get_cell(p[0], q) == 0:
                q += 1
        elif col_dir == -1 and row_dir == 1:
            while grid.get_cell(p[0] - 1, q - 1) == 0:
                q -= 1
        elif col_dir == -1 and row_dir == -1:
            while grid.get_cell(p[0], q - 1) == 0:
                q -= 1

        I_max = (Fraction(min(p[1], q)), Fraction(max(p[1], q)), row + row_dir)
        # print("flat I_max col_dir row_dir", I_max, col_dir, row_dir)

    else:
        # Non-observable successors of a cone node

        p: tp.Tuple[int, Fraction] = (row + row_dir,
                                      root[1] + Fraction(a - root[1], abs(root[0]-row)) * abs(row + row_dir - root[0]))

        if col_dir == 1:

            if p[1] < a:
                x = a
                while x > p[1]:
                    if grid.get_cell(row - (row_dir == -1), x - 1) != 0:
                        q = x
                        I_max = (Fraction(q), Fraction(a), row + row_dir)
                        break
                    x -= 1
                else:
                    q = -1
                    I_max = (p[1], Fraction(a), row + row_dir)
            else:
                x = a
                while x < p[1]:
                    if grid.get_cell(row - (row_dir == -1), x) != 0:
                        return []
                    x += 1
                q = ceil(p[1])
                while grid.get_cell(row - (row_dir == -1), q) == 0:
                    q += 1
                I_max = (p[1], Fraction(q), row + row_dir)

        else:  # col_dir == -1:

            if p[1] > a:
                x = a
                while x < p[1]:
                    if grid.get_cell(row - (row_dir == -1), x) != 0:
                        q = x
                        I_max = (Fraction(a), Fraction(q), row + row_dir)
                        break
                    x += 1
                else:
                    q = -1
                    I_max = (Fraction(a), p[1], row + row_dir)
            else:
                x = a
                while x > p[1]:
                    if grid.get_cell(row - (row_dir == -1), x - 1) != 0:
                        return []
                    x -= 1
                q = floor(p[1])
                while grid.get_cell(row - (row_dir == -1), q - 1) == 0:
                    q -= 1
                I_max = (Fraction(q), p[1], row + row_dir)

        # print("I_max a p q row_dir col_dir", I_max, a, p, q, row_dir, col_dir)

    successors = []
    for (l, r, row) in split_interval_at_corner_points(grid, I_max):
        g_value = root_dist + dist
        successors.append(Node((l, r), row, new_root, g_value,
                               f_value=calculate_f_value((l, r), row, new_root, g_value, target)))

        # print("non-obs-succs", (l, r), row, new_root)

    return successors


def generate_observable_cone_successors(grid: Map, interval: tp.Tuple[Fraction, Fraction], row: int,
                                        root: tp.Tuple[int, int], root_dist: float,
                                        target: tp.Tuple[int, int]) -> tp.List[Node]:
    row_dir = 1 if root[0] < row else -1

    if row + row_dir < 0 or row + row_dir > grid.height:
        return []

    if any(grid.get_cell(row - (row_dir == -1), i) != 0 for i in range(floor(interval[0]), ceil(interval[1]))):
        return []

    if interval[0] == interval[1] and interval[0].denominator == 1 and \
            grid.is_between_obstacles(row, interval[0].numerator):
        return []

    if interval[0] == interval[1] and interval[0].denominator == 1 and \
            grid.get_cell(row - (row_dir == -1), interval[0].numerator - 1) != 0 and \
            grid.get_cell(row - (row_dir == -1), interval[0].numerator) != 0:
        return []

    l = root[1] + (interval[0] - root[1]) / abs(root[0] - row) * (abs(root[0] - row) + 1)
    l = max(l, 0)
    if l > grid.width:
        return []
    r = root[1] + (interval[1] - root[1]) / abs(root[0] - row) * (abs(root[0] - row) + 1)
    if r < 0:
        return []
    r = min(r, grid.width)

    if r > interval[1]:
        x = ceil(interval[1])
        while x < r:
            if grid.get_cell(row - (row_dir == -1), x) != 0:
                r = Fraction(x)
                break
            x += 1
    elif r < interval[1]:
        x = floor(interval[1])
        while x > r:
            if grid.get_cell(row - (row_dir == -1), x - 1) != 0:
                return []
            x -= 1

    if l > interval[0]:
        x = ceil(interval[0])
        while x < l:
            if grid.get_cell(row - (row_dir == -1), x) != 0:
                return []
            x += 1
    elif l < interval[0]:
        x = floor(interval[0])
        while x > l:
            if grid.get_cell(row - (row_dir == -1), x - 1) != 0:
                l = Fraction(x)
                break
            x -= 1

    I_max: tp.Tuple[Fraction, Fraction, int] = (l, r, row + row_dir)
    # print("obs cone I_max", I_max)
    successors = []
    for (l, r, row) in split_interval_at_corner_points(grid, I_max):
        successors.append(Node((l, r), row, root, root_dist,
                               f_value=calculate_f_value((l, r), row, root, root_dist, target)))

    return successors


def turning_point_check(grid: Map, p1: tp.Tuple[int, Fraction],
                        r: tp.Tuple[int, int]) -> tuple[bool, tp.Literal[-1, 1], tp.Literal[-1, 1]]:
    """
    :return: (is_turning_point, row_direction (up/down), column_direction (left/right))
    """

    if p1[1].denominator != 1:
        return False, 1, 1

    p: tp.Tuple[int, int] = (p1[0], p1[1].numerator)

    if not grid.is_corner_point(p[0], p[1]):
        return False, 1, 1

    if r[0] < p[0] and r[1] < p[1]:

        if grid.get_cell(p[0], p[1] - 1) == 1:
            return True, 1, -1
        elif grid.get_cell(p[0] - 1, p[1]) == 1:
            return True, 1, 1
        else:
            return False, 1, 1

    elif r[0] < p[0] and r[1] == p[1]:

        if grid.get_cell(p[0] - 1, p[1] - 1) == 1:
            return True, 1, -1
        elif grid.get_cell(p[0] - 1, p[1]) == 1:
            return True, 1, 1
        else:
            return False, 1, 1

    elif r[0] < p[0] and r[1] > p[1]:

        if grid.get_cell(p[0] - 1, p[1] - 1) == 1:
            return True, 1, -1
        elif grid.get_cell(p[0], p[1]) == 1:
            return True, 1, 1
        else:
            return False, 1, 1

    elif r[0] == p[0] and r[1] > p[1]:

        if grid.get_cell(p[0], p[1]) == 1:
            return True, 1, -1
        elif grid.get_cell(p[0] - 1, p[1]) == 1:
            return True, -1, -1
        else:
            return False, 1, 1

    elif r[0] > p[0] and r[1] > p[1]:

        if grid.get_cell(p[0] - 1, p[1]) == 1:
            return True, -1, 1
        elif grid.get_cell(p[0], p[1] - 1) == 1:
            return True, -1, -1
        else:
            return False, 1, 1

    elif r[0] > p[0] and r[1] == p[1]:

        if grid.get_cell(p[0], p[1] - 1) == 1:
            return True, -1, -1
        elif grid.get_cell(p[0], p[1]) == 1:
            return True, -1, 1
        else:
            return False, 1, 1

    elif r[0] > p[0] and r[1] < p[1]:

        if grid.get_cell(p[0] - 1, p[1] - 1) == 1:
            return True, -1, -1
        elif grid.get_cell(p[0], p[1]) == 1:
            return True, -1, 1
        else:
            return False, 1, 1

    elif r[0] == p[0] and r[1] < p[1]:

        if grid.get_cell(p[0] - 1, p[1] - 1) == 1:
            return True, -1, 1
        if grid.get_cell(p[0], p[1] - 1) == 1:
            return True, 1, 1
        else:
            return False, 1, 1

    elif r[0] == p[0] and r[1] == p[1]:
        return False, 1, 1

    else:
        assert False, "Not reachable"


def generate_successors(grid: Map, node: Node, target: tp.Tuple[int, int]) -> tp.List[Node]:
    if node.is_start:
        return generate_start_successors(grid, (node.row, node.interval[1].numerator), target)

    successors = []

    if node.is_flat_node:
        p: tp.Tuple[int, Fraction]
        if abs(node.interval[0] - node.root[1]) > abs(node.interval[1] - node.root[1]):
            p = (node.row, node.interval[0])
        else:
            p = (node.row, node.interval[1])

        # generate observable flat successors
        col_dir: tp.Literal[-1, 1] = 1 if p[1] > node.root[1] else -1
        successors += generate_flat_successors(grid, p, node.root, col_dir, node.g_value, target)

        # for x in successors:
        #    print("obs succ", x.row, x.interval, x.root, x.is_empty())
        # sz = len(successors)

        # generate non-observable cone successors if p is a turning point
        is_turning_point, row_dir, col_dir = turning_point_check(grid, p, node.root)
        if is_turning_point:
            assert p[1].denominator == 1
            successors += generate_non_observable_cone_successors(grid, node.row, p[1].numerator,
                                                                  node.root, row_dir, col_dir, node.g_value, target)

        # for x in successors[sz:]:
        #    print("non-obs succ", x.row, x.interval, x.root, x.is_empty(), x.g_value, x.f_value)

    else:
        a: tp.Tuple[int, Fraction] = (node.row, node.interval[0])
        b: tp.Tuple[int, Fraction] = (node.row, node.interval[1])

        successors += generate_observable_cone_successors(grid, node.interval, node.row, node.root, node.g_value,
                                                          target)

        # for x in successors:
        #    print("obs succ", x.row, x.interval, x.root, x.is_empty())
        sz = len(successors)

        # generate non-observable successors if a is a turning point
        is_turning_point, row_dir, col_dir = turning_point_check(grid, a, node.root)
        if is_turning_point:
            # print("dir", node.root, a, row_dir, col_dir)
            successors += generate_flat_successors(grid, a, node.root, col_dir, node.g_value, target)
            assert a[1].denominator == 1
            successors += generate_non_observable_cone_successors(grid, a[0], a[1].numerator, node.root,
                                                                  row_dir, col_dir, node.g_value, target)

        # generate non-observable successors if b is a turning point
        is_turning_point, row_dir, col_dir = turning_point_check(grid, b, node.root)
        if is_turning_point:
            # print("dir", node.root, b, row_dir, col_dir)
            successors += generate_flat_successors(grid, b, node.root, col_dir, node.g_value, target)
            assert b[1].denominator == 1
            successors += generate_non_observable_cone_successors(grid, b[0], b[1].numerator, node.root,
                                                                  row_dir, col_dir, node.g_value, target)

        # for x in successors[sz:]:
        #    print("non-obs succ", x.row, x.interval, x.root, x.is_empty(), x.g_value, x.f_value)

    return successors


def get_path(target: tp.Tuple[int, int], last_node: Node) -> tp.List[tp.Tuple[int, int]]:
    result = [target, last_node.root]
    while last_node.parent is not None:
        last_node = last_node.parent
        if last_node.root != result[-1]:
            result.append(last_node.root)
    result.pop()
    result.reverse()
    return result


INF = 10 ** 9


def anya(grid: Map, source: tp.Tuple[int, int],
         target: tp.Tuple[int, int], interface: int = 0)\
        -> tp.Union[tp.Tuple[bool, tp.Optional[Node], Stats], tp.Tuple[float, tp.List[tp.Tuple[int, int]]]]:

    stats = Stats()
    start = time.time()
    stats.max_tree_size = 1

    start_node = Node((Fraction(source[1]), Fraction(source[1])), source[0], (-1, -1),
                      g_value=0, f_value=euclidean_distance(source, target), is_start=True)

    if source == target and interface == 0:
        stats.runtime = time.time() - start
        stats.way_length = 0
        return True, start_node, stats
    elif source == target:
        return 0, [source]

    open_: tp.List[Node] = [start_node]
    heapify(open_)
    root_history: tp.Dict[tp.Tuple[int, int], float] = defaultdict(lambda: INF)
    put_in_open: tp.Set[Node] = set()

    while len(open_) > 0:
        cur = heappop(open_)
        stats.expansions += 1
        # print(cur.root, cur.interval, cur.row, cur.g_value, cur.f_value)

        if cur.contains_point(target):
            # path found
            stats.runtime = time.time() - start
            stats.way_length = cur.g_value + euclidean_distance(cur.root, target)
            if interface == 0:
                return True, cur, stats
            else:
                return cur.g_value + euclidean_distance(cur.root, target), get_path(target, cur)

        for succ in generate_successors(grid, cur, target):
            if succ.is_empty():
                continue

            old_g_value = root_history[succ.root]
            if old_g_value < succ.g_value or succ in put_in_open:
                continue
            succ.parent = cur
            root_history[succ.root] = succ.g_value
            heappush(open_, succ)
            put_in_open.add(succ)
            stats.max_tree_size += 1  # TODO

    stats.runtime = time.time() - start
    # path not found
    if interface == 0:
        return False, None, stats
    else:
        return -1, []

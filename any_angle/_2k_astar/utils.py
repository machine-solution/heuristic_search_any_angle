import numpy as np
from heapq import heappop, heappush


# rectangle (n x m), n >= m > 0
def simple_intersect_cells(n, m):
    cells = []

    for i in range(0, n):
        y = i * m // n
        x = i
        cells.append((x, y))
        if x > 0:
            cells.append((x - 1, y))
        if y > 0 and y * n == i * m and y >= 0:
            cells.append((x, y - 1))
            if x > 0:
                cells.append((x - 1, y - 1))
    return cells


def intersect_cells(i1, j1, i2, j2):
    cells = []
    start = (i1, j1)

    s1 = 1
    l1 = 0
    if i1 > i2:
        s1 = -1
        l1 = -1
        i1, i2 = i2, i1

    s2 = 1
    l2 = 0
    if j1 > j2:
        s2 = -1
        l2 = -1
        j1, j2 = j2, j1

    r = 0
    if j2 - j1 > i2 - i1:
        r = 1
        i1, i2, j1, j2 = j1, j2, i1, i2
        s1, s2 = s2, s1
        l1, l2 = l2, l1

    n = i2 - i1
    m = j2 - j1
    s_cells = simple_intersect_cells(n, m)
    for cell in s_cells:
        if r == 1:
            cells.append((start[0] + cell[1] * s2 + l2, start[1] + cell[0] * s1 + l1))
        else:
            cells.append((start[0] + cell[0] * s1 + l1, start[1] + cell[1] * s2 + l2))
    return cells


def vect_product(i1, j1, i2, j2):
    return i1 * j2 - j1 * i2


def scalar_product(i1, j1, i2, j2):
    return i1 * i2 + j1 * j2


def length(i, j):
    return np.sqrt(i**2 + j**2)


def euclidian_distance(i1, j1, i2, j2, *args):
    return length(i1 - i2, j1 - j2)


def compute_cost(i1, j1, i2, j2):
    return length(i1 - i2, j1 - j2)


def h_2k(i1, j1, i2, j2, k):
    x = abs(i2 - i1)
    y = abs(j2 - j1)
    l = [1, 0]
    r = [0, 1]
    for _ in range(k - 2):
        if x > y:
            r[0] += l[0]
            r[1] += l[1]
            x -= y
        else:
            l[0] += r[0]
            l[1] += r[1]
            y -= x
    return x * length(*l) + y * length(*r)


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
        return str(self.difficulty) + delimiter + str(self.expansions) + delimiter + str(
            self.runtime) + delimiter + str(self.way_length) + \
               delimiter + str(self.suboptimal) + delimiter + str(self.max_tree_size)

    def header(self):
        delimiter = ","
        return "difficulty" + delimiter + "expansions" + delimiter + "runtime" + delimiter + "way_length" + \
               delimiter + "suboptimal" + delimiter + "max_tree_size"


class SearchTreePQS:  # SearchTree which uses PriorityQueue for OPEN and set for CLOSED

    def __init__(self):
        self._open = []
        self._closed = set()
        self._true_value_computed = set()
        self._enc_open_dublicates = 0

    def __len__(self):
        return len(self._open) + len(self._closed)

    def remove_open_dublicates(self):
        while len(self._open) and self._open[0] in self._closed:
            heappop(self._open)

    def open_is_empty(self):
        self.remove_open_dublicates()
        return len(self._open) == 0

    def add_to_open(self, item):
        heappush(self._open, item)

    def get_best_node_from_open(self):
        self.remove_open_dublicates()
        return None if self.open_is_empty() else heappop(self._open)

    def add_to_closed(self, item):
        self._closed.add(item)

    def was_expanded(self, item):
        return item in self._closed

    @property
    def OPEN(self):
        return self._open

    @property
    def CLOSED(self):
        return self._closed

    @property
    def number_of_open_dublicates(self):
        return self._enc_open_dublicates


def make_path(goal):
    '''
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    '''

    length_ = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length_

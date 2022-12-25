import numpy as np
from heapq import heappop, heappush


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
    """
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    """

    length_ = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length_

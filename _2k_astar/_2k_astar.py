from heapq import heappop, heappush
import time

from .utils import compute_cost


class Node:
    '''
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node
    - F: f-value of the node
    - parent: pointer to the parent-node

    '''

    def __init__(self, i, j, g=0, h=0, f=None, parent=None, number_of_move=None, tie_breaking_func=None):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        if f is None:
            self.f = self.g + h
        else:
            self.f = f
        self.parent = parent
        self.number_of_move = number_of_move

    def __eq__(self, other):
        '''
        Estimating where the two search nodes are the same,
        which is needed to detect dublicates in the search tree.
        '''
        return (self.i == other.i) and (self.j == other.j)

    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        ij = self.i, self.j
        return hash(ij)

    def __lt__(self, other):
        '''
        Comparing the keys (i.e. the f-values) of two nodes,
        which is needed to sort/extract the best element from OPEN.

        This comparator is very basic. We will code a more plausible comparator further on.
        '''
        return self.f < other.f


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


# using for counting statistics and returning it as one variable
class Stats:
    def __init__(self):
        self.difficulty = 0
        self.expansions = 0 # algorithm must set this value
        self.runtime = 0 # algorithm must set this value
        self.way_length = 0 # algorithm must set this value
        self.suboptimal = 0
        self.max_tree_size = 0 # algorithm must set this value

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
        return str(self.difficulty) + delimiter + str(self.expansions) + delimiter + str(self.runtime) + delimiter + str(self.way_length) +\
        delimiter + str(self.suboptimal)  + delimiter + str(self.max_tree_size)
    
    def header(self):
        delimiter = ","
        return "difficulty" + delimiter + "expansions" + delimiter + "runtime" + delimiter + "way_length" +\
        delimiter + "suboptimal" + delimiter + "max_tree_size"


def astar(grid_map, start_i, start_j, goal_i, goal_j, heuristic_func=None, search_tree=None, w=1, k=2):
    stats = Stats()
    stats.runtime = time.time()
    ast = search_tree()
    goal_node = Node(goal_i, goal_j)
    path_found = False

    ast.add_to_open(Node(start_i, start_j,
                         h=w * heuristic_func(start_i, start_j, goal_i, goal_j, k)
                         if heuristic_func else 0))
    while not ast.open_is_empty():
        stats.max_tree_size = max(stats.max_tree_size, len(ast))
        curr_node = ast.get_best_node_from_open()
        ast.add_to_closed(curr_node)
        if curr_node == goal_node:
            path_found = True
            goal_node = curr_node  # define g*-value in variable
            break
        stats.expansions += 1
        for i, j in grid_map.get_neighbors(curr_node.i, curr_node.j, k):
            nxt_node = Node(i, j, g=curr_node.g + compute_cost(curr_node.i, curr_node.j, i, j),
                            h=w * heuristic_func(i, j, goal_i, goal_j, k)
                            if heuristic_func else 0,
                            parent=curr_node)
            if not ast.was_expanded(nxt_node):
                ast.add_to_open(nxt_node)
    stats.max_tree_size = max(stats.max_tree_size, len(ast))

    if not path_found:
        goal_node = None
    else:
        stats.way_length = goal_node.g
    stats.runtime = time.time() - stats.runtime
    return path_found, goal_node, stats, ast.OPEN, ast.CLOSED


def canonical_astar(grid_map, start_i, start_j, goal_i, goal_j, heuristic_func=None, search_tree=None, w=1, k=2):
    stats = Stats()
    stats.runtime = time.time()
    ast = search_tree()
    goal_node = Node(goal_i, goal_j)
    path_found = False

    ast.add_to_open(Node(start_i, start_j,
                         h=w * heuristic_func(start_i, start_j, goal_i, goal_j, k)
                         if heuristic_func else 0))
    while not ast.open_is_empty():
        stats.max_tree_size = max(stats.max_tree_size, len(ast))
        curr_node = ast.get_best_node_from_open()
        ast.add_to_closed(curr_node)
        if curr_node == goal_node:
            path_found = True
            goal_node = curr_node  # define g*-value in variable
            break
        stats.expansions += 1
        neighbors = grid_map.get_natural_neighbors(curr_node.i, curr_node.j, curr_node.number_of_move, k) + \
                    grid_map.get_forced_neighbors(curr_node.i, curr_node.j, curr_node.number_of_move, k)
        for i, j, num in neighbors:
            nxt_node = Node(i, j, g=curr_node.g + compute_cost(curr_node.i, curr_node.j, i, j),
                            h=w * heuristic_func(i, j, goal_i, goal_j, k)
                            if heuristic_func else 0,
                            parent=curr_node, number_of_move=num)
            if not ast.was_expanded(nxt_node):
                ast.add_to_open(nxt_node)
    stats.max_tree_size = max(stats.max_tree_size, len(ast))

    if not path_found:
        goal_node = None
    else:
        stats.way_length = goal_node.g
    stats.runtime = time.time() - stats.runtime
    return path_found, goal_node, stats, ast.OPEN, ast.CLOSED

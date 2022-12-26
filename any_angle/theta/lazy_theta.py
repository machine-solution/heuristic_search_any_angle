from datetime import datetime
import math

from .utils import compute_cost
from .theta import Node, make_path
from ..common.api import Stats


class LazyNode(Node):
    def __init__(self, i, j, g=0, h=0, f=None, parent=None, lazy_parent=None, true_node=False):
        self.i = i
        self.j = j
        self.parent = parent
        self.lazy_parent = lazy_parent
        self.true_node = true_node
        self.g = g
        self.h = h
        if f is None:
            self.f = self.g + h
        else:
            self.f = f
        self.tie = math.inf

    # recount true g-value using a parent
    # recount true f-value using true g-value as well        
    def recount_g(self, grid_map):
        if self.parent is None:
            return

        if grid_map.visible(self.i, self.j, self.parent.i, self.parent.j):
            pass
        else:
            self.parent = self.lazy_parent

        self.g = self.parent.g + compute_cost(self.i, self.j, self.parent.i, self.parent.j)
        self.true_node = True
        self.f = self.g + self.h


def getSuccessor(node, i, j, grid_map, goal_i, goal_j, heuristic_func, w):
    suc = LazyNode(i, j, g=node.parent.g + compute_cost(node.parent.i, node.parent.j, i, j),
                   parent=node.parent, lazy_parent=node, true_node=False)
    suc.apply_heuristic(heuristic_func, goal_i, goal_j, w)
    return suc


def getSuccessors(node, grid_map, goal_i, goal_j, heuristic_func, w, k):
    neighbors = grid_map.get_neighbors(node.i, node.j, k)
    successors = []
    for cell in neighbors:
        successors.append(getSuccessor(node, cell[0], cell[1], grid_map, goal_i, goal_j, heuristic_func, w))
    return successors


def lazy_theta(grid_map, start_i, start_j, goal_i, goal_j, heuristic_func=None, search_tree=None, w=1, k=8):
    start_time = datetime.now()  # statistic

    stats = Stats()  # statistic

    grid_map.add_special_point((goal_i, goal_j))

    ast = search_tree()
    start = LazyNode(start_i, start_j, g=0, parent=None, lazy_parent=None, true_node=True)
    start.parent = start
    start.lazy_parent = start
    start.apply_heuristic(heuristic_func, goal_i, goal_j, w)
    start.parent = start
    ast.add_to_open(start)

    while not ast.open_is_empty():
        curr = ast.get_best_node_from_open()
        if curr is None:
            break
        elif not curr.true_node:
            curr.recount_g(grid_map)
            curr.apply_heuristic(heuristic_func, goal_i, goal_j, w)  # h may be changed with changing parent
            ast.add_to_open(curr)
            # to do this code easier we want add this node to open and not check 
            # if it is really best
            continue

        ast.add_to_closed(curr)

        if (curr.i == goal_i) and (curr.j == goal_j):  # curr is goal
            stats.runtime = datetime.now() - start_time  # statistic
            path, stats.way_length = make_path(curr)  # statistic
            stats.path_found = True
            stats.path = [(x.i, x.j) for x in path]
            return True, curr, stats, ast.OPEN, ast.CLOSED

        # expanding curr
        stats.expansions += 1  # statistic
        successors = getSuccessors(curr, grid_map, goal_i, goal_j, heuristic_func, w, k)

        for node in successors:
            if not ast.was_expanded(node):
                ast.add_to_open(node)

        stats.max_tree_size = max(stats.max_tree_size, len(ast))  # statistic

    stats.runtime = datetime.now() - start_time  # statistic
    stats.way_length = 0  # statistic
    return False, None, stats, ast.OPEN, ast.CLOSED

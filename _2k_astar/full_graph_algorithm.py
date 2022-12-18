from .utils import compute_cost, Stats
from .grid import Map, Node
import time


def gcd(a, b):
    if b:
        return gcd(b, a % b)
    return a


class MapFullGraph(Map):
    def __init__(self):
        super().__init__()

    def get_neighbors(self, i, j):
        neighbors = []
        for i1 in range(self._height + 1):
            for j1 in range(self._width + 1):
                if (i1, j1) == (i, j):
                    continue
                if gcd(abs(i1 - i), abs(j1 - j)) != 1:
                    continue
                if not self.move_is_correct(i, j, i1, j1):
                    continue
                neighbors.append((i1, j1))
        return neighbors


def full_graph_astar(grid_map, start_i, start_j, goal_i, goal_j, heuristic_func=None, search_tree=None):
    stats = Stats()
    stats.runtime = time.time()
    ast = search_tree()
    goal_node = Node(goal_i, goal_j)
    path_found = False

    ast.add_to_open(Node(start_i, start_j,
                         h=heuristic_func(start_i, start_j, goal_i, goal_j)
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
        for i, j in grid_map.get_neighbors(curr_node.i, curr_node.j):
            nxt_node = Node(i, j, g=curr_node.g + compute_cost(curr_node.i, curr_node.j, i, j),
                            h=heuristic_func(i, j, goal_i, goal_j)
                            if heuristic_func else 0,
                            parent=curr_node)
            if nxt_node == goal_node:
                path_found = True
                goal_node = nxt_node  # define g*-value in variable
                break
            if grid_map.diagonal_obstacles(nxt_node.i, nxt_node.j):
                continue
            if not ast.was_expanded(nxt_node):
                ast.add_to_open(nxt_node)
        else:
            continue
        break
    stats.max_tree_size = max(stats.max_tree_size, len(ast))

    if not path_found:
        goal_node = None
    else:
        stats.way_length = goal_node.g
    stats.runtime = time.time() - stats.runtime
    return path_found, goal_node, stats, ast.OPEN, ast.CLOSED

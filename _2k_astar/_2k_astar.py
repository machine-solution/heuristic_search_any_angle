import time
from grid import Map, Node
from utils import compute_cost, vect_product, scalar_product, Stats


class Map_2k(Map):
    def __init__(self, k):
        super().__init__()
        self._delta = []
        self._k = k
        self._make_delta()

    def _make_delta(self):
        '''
        Generate all directions in clockwise order, starting with (-1, 0).
        '''
        delta = [(-1, 0), (0, 1)]
        for _ in range(self._k - 2):
            new_delta = []
            for i in range(len(delta) - 1):
                new_direction = (delta[i][0] + delta[i + 1][0], delta[i][1] + delta[i + 1][1])
                new_delta.append(delta[i])
                new_delta.append(new_direction)
            new_delta.append(delta[-1])
            delta = new_delta
        delta.pop(-1)
        for elem in delta:
            self._delta.append(elem)
        for elem in delta:
            self._delta.append((elem[1], -elem[0]))
        for elem in delta:
            self._delta.append((-elem[0], -elem[1]))
        for elem in delta:
            self._delta.append((-elem[1], elem[0]))

    def get_neighbors(self, i, j, number_of_prev_move=None):
        return self.get_natural_neighbors(i, j, number_of_prev_move) + \
               self.get_forced_neighbors(i, j, number_of_prev_move)

    def get_natural_neighbors(self, i, j, number_of_prev_move=None):
        neighbors = []

        if number_of_prev_move is None:
            for ind, d in enumerate(self._delta):
                if self.move_is_correct(i, j, i + d[0], j + d[1]):
                    neighbors.append((i + d[0], j + d[1], ind))
            return neighbors

        if number_of_prev_move % 2:
            for ind in range(-1, 2):
                number_of_current_move = (number_of_prev_move + ind + 2 ** self._k) % 2 ** self._k
                d = self._delta[number_of_current_move]
                if self.move_is_correct(i, j, i + d[0], j + d[1]):
                    neighbors.append((i + d[0], j + d[1], number_of_current_move))
        else:
            d = self._delta[number_of_prev_move]
            if self.move_is_correct(i, j, i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1], number_of_prev_move))
        return neighbors

    def get_forced_neighbors(self, i, j, number_of_prev_move=None):
        '''
        Can intersect with natural neighbors by no more then one
        direction but that is doesn't affect algorithm's correctness.
        '''
        if number_of_prev_move is None:
            return []

        if sum(self.neighbor_obstacles(i, j)) != 1:
            return []

        neighbors = []
        # next indexes are of ortogonal moves around an obstacle
        m1_ind = -1
        m2_ind = -1
        for ind, cell in enumerate(self.neighbor_cells(i, j)):
            if not self.traversable(*cell):
                m1_ind = ind * 2 ** (self._k - 2)
                m2_ind = ((ind + 1) % 4) * 2 ** (self._k - 2)
                break
        v1 = vect_product(*self._delta[m1_ind], *self._delta[number_of_prev_move])
        v2 = vect_product(*self._delta[m2_ind], *self._delta[number_of_prev_move])
        if v1 * v2 < 0 or m1_ind == number_of_prev_move or m2_ind == number_of_prev_move:
            return []
        s1 = scalar_product(*self._delta[m1_ind], *self._delta[number_of_prev_move])
        s2 = scalar_product(*self._delta[m2_ind], *self._delta[number_of_prev_move])
        if s1 > s2:
            ind1 = number_of_prev_move + 1
            ind2 = m1_ind
        else:
            ind1 = m2_ind
            ind2 = number_of_prev_move - 1
        if ind1 > ind2:
            ind2 += 2 ** self._k
        for ind in range(ind1, ind2 + 1):
            number_of_current_move = ind % 2**self._k
            d = self._delta[number_of_current_move]
            if self.move_is_correct(i, j, i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1], number_of_current_move))
        return neighbors


class Node_2k(Node):
    def __init__(self, *args, **kwargs):
        if "number_of_move" in kwargs:
            self.number_of_move = kwargs.pop("number_of_move")
        else:
            self.number_of_move = None
        super().__init__(*args, **kwargs)


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
        for i, j, num in grid_map.get_neighbors(curr_node.i, curr_node.j):
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
    goal_node = Node_2k(goal_i, goal_j)
    path_found = False

    ast.add_to_open(Node_2k(start_i, start_j,
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
        for i, j, num in grid_map.get_neighbors(curr_node.i, curr_node.j, curr_node.number_of_move):
            nxt_node = Node_2k(i, j, g=curr_node.g + compute_cost(curr_node.i, curr_node.j, i, j),
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


def path_is_canonical(grid_map, goal_node, k):
    node = goal_node
    prev_number = node.number_of_move
    node = node.parent
    while node and node.number_of_move:
        numbers_delta = min(abs(node.number_of_move - prev_number),
                            2**k - abs(node.number_of_move - prev_number))
        if not numbers_delta:
            node = node.parent
            continue
        if prev_number % 2 == 0 and numbers_delta == 1:
            prev_number = node.number_of_move
            node = node.parent
            continue
        if sum(grid_map.neighbor_obstacles(node.i, node.j)) == 1:
            prev_number = node.number_of_move
            node = node.parent
            continue
        return False
    return True

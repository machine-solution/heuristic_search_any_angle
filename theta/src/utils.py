from math import sqrt


def compute_cost(i1, j1, i2, j2):
    '''
    Computes cost of moves between cells
    '''
    return sqrt(abs(i1 - i2) ** 2 + abs(j1 - j2) ** 2)


def euclidian_distance(node, goal_i, goal_j):
    
    return compute_cost(node.i, node.j, goal_i, goal_j)


def theta_heuristic(node, goal_i, goal_j):
    return max(0, node.parent.g + compute_cost(node.parent.i, node.parent.j, goal_i, goal_j))


class Stats:
    def __init__(self):
        self.difficulty = 0
        self.expansions = 0 # algorithm must set this value
        self.runtime = 0 # algorithm must set this value
        self.way_length = 0 # algorithm must set this value
        self.suboptimal = 0
        self.max_tree_size = 0 # algorithm must set this value

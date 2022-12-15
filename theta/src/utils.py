from math import sqrt
import math


def length(i1, i2):
    return sqrt(i1 ** 2 + i2 ** 2)


def dist(i1, j1, i2, j2):
    return sqrt(abs(i1 - i2) ** 2 + abs(j1 - j2) ** 2)


# for nodes
def dist_n(a, b):
    return dist(a.i, a.j, b.i, b.j)


def cross_product(i1, j1, i2, j2):
    return i1 * j2 - i2 * j1


def angle(ax, ay, ox, oy, bx, by):
    if ax == ox and ay == oy:
        return 0

    if bx == ox and by == oy:
        return 0

    return math.asin(cross_product(ax - ox, ay - oy, bx - ox, by - oy) / (length(ax - ox, ay - oy) * length(bx - ox, by - oy)))


# for nodes
def angle_n(a, o, b):
    return angle(a.i, a.j, o.i, o.j, b.i, b.j)


def compute_cost(i1, j1, i2, j2):
    return dist(i1, j1, i2, j2)


def euclidian_distance(node, goal_i, goal_j):
    
    return dist(node.i, node.j, goal_i, goal_j)


def theta_heuristic(node, goal_i, goal_j):
    return max(0, node.parent.g + compute_cost(node.parent.i, node.parent.j, goal_i, goal_j))


def weighted_heuristic(node, goal_i, goal_j):
    a = 0.9
    
    return a * euclidian_distance(node, goal_i, goal_j) +  (1 - a) * theta_heuristic(node, goal_i, goal_j)

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


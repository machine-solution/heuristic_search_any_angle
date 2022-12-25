import math


def length(i1, i2):
    return (i1 ** 2 + i2 ** 2) ** 0.5


def dist(i1, j1, i2, j2):
    return (abs(i1 - i2) ** 2 + abs(j1 - j2) ** 2) ** 0.5


def sqr_dist(i1, j1, i2, j2):
    return abs(i1 - i2) ** 2 + abs(j1 - j2) ** 2


def sqr_dist_n(a, b):
    return sqr_dist(a.i, a.j, b.i, b.j)


# for nodes
def dist_n(a, b):
    return dist(a.i, a.j, b.i, b.j)


def cross_product(i1, j1, i2, j2):
    return i1 * j2 - i2 * j1


def scalar_product(i1, j1, i2, j2):
    return i1 * i2 + j1 * j2


def angle(ax, ay, ox, oy, bx, by):
    if ax == ox and ay == oy:
        return 0

    if bx == ox and by == oy:
        return 0

    return math.asin(cross_product(ax - ox, ay - oy, bx - ox, by - oy) / (length(ax - ox, ay - oy) * length(bx - ox, by - oy)))


class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __repr__(self):
        return "(" + str(self.i) + ", " + str(self.j) + ")"

    def __sub__(self, other):
        return Vector(self.i - other.i, self.j- other.j)


# comparators for rays
class Vector:
    # inf == 0 means not \infty, inf == 1 means +\infty, inf == -1 means  -\infty
    def __init__(self, i, j, inf=0):
        self.i = i
        self.j = j
        self.inf = inf

    def __repr__(self):
        if self.inf > 0:
            return "+infty"
        if self.inf < 0:
            return "-infty"
        return "(" + str(self.i) + ", " + str(self.j) + ")"

    def length(self):
        return length(self.i, self.j)

    def angle_rad(self, i, j):
        alpha = angle(i, j, 0, 0, self.i, self.j)
        if scalar_product(self.i, self.j, i, j) < 0:
            if alpha < 0:
                return -math.pi - alpha
            else:
                return math.pi - alpha
        else:
            return alpha

    def angle_deg(self, i, j):
        alpha = angle(i, j, 0, 0, self.i, self.j) * 180 / math.pi
        if scalar_product(self.i, self.j, i, j) < 0:
            if alpha < 0:
                return -math.pi - alpha
            else:
                return math.pi - alpha
        else:
            return alpha

    def __add__(self, other):
        return Vector(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        return Vector(self.i - other.i, self.j- other.j)

    def __lt__(self, other):
        if self.inf != other.inf:
            return self.inf < other.inf
        return cross_product(self.i, self.j, other.i, other.j) < 0

    def __gt__(self, other):
        if self.inf != other.inf:
            return self.inf > other.inf
        return cross_product(self.i, self.j, other.i, other.j) > 0

    def __le__(self, other):
        if self.inf != other.inf:
            return self.inf <= other.inf
        return cross_product(self.i, self.j, other.i, other.j) <= 0

    def __ge__(self, other):
        if self.inf != other.inf:
            return self.inf >= other.inf
        return cross_product(self.i, self.j, other.i, other.j) >= 0

    def __eq__(self, other):
        if self.inf != other.inf:
            return self.inf == other.inf
        return cross_product(self.i, self.j, other.i, other.j) == 0


# for nodes
def angle_n(a, o, b):
    return angle(a.i, a.j, o.i, o.j, b.i, b.j)


def compute_cost(i1, j1, i2, j2):
    return dist(i1, j1, i2, j2)


def compute_cost_n(a, b):
    return dist(a.i, a.j, b.i, b.j)


def euclidian_distance(node, goal_i, goal_j, wh = 0.1):
    
    return dist(node.i, node.j, goal_i, goal_j)


def theta_heuristic(node, goal_i, goal_j, wh = 0.1):
    return max(0, node.parent.g + compute_cost(node.parent.i, node.parent.j, goal_i, goal_j))


def weighted_heuristic(node, goal_i, goal_j, wh = 0.1):
    return (1 - wh) * euclidian_distance(node, goal_i, goal_j) +  wh * theta_heuristic(node, goal_i, goal_j)


def tie_break_heuristic(node, goal_i, goal_j):
    return euclidian_distance(node, goal_i, goal_j), theta_heuristic(node, goal_i, goal_j)

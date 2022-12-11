import numpy as np


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

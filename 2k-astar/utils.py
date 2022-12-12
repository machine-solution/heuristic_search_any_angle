import numpy as np


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

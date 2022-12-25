# rectangle (n x m), n >= m > 0
def simple_intersect_cells(n, m):
    cells = []

    for x in range(0, n):
        y = x * m // n
        cells.append((x, y))
        if y * n == x * m:
            continue
        if x > 0:
            cells.append((x - 1, y))
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


def gcd(a, b):
    a = abs(a)
    b = abs(b)
    while b > 0:
        a %= b
        a, b = b, a
    return a


def intersect_points(i1, j1, i2, j2):
    g = gcd(i2 - i1, j2 - j1)
    if g == 0:
        return []
    dx = (i2 - i1) // g
    dy = (j2 - j1) // g
    points = []
    i1 += dx
    j1 += dy
    while i1 != i2:
        points.append((i1, j1))
        i1 += dx
        j1 += dy
    return points


def vect_product(i1, j1, i2, j2):
    return i1 * j2 - j1 * i2

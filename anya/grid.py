import typing as tp


class Map:
    def __init__(self):
        '''
        Default constructor
        '''

        self._width = 0
        self._height = 0
        self.height = 0
        self.width = 0
        self._cells = []

    def read_from_string(self, cell_str: str, width: int, height: int):
        """
        Convert a string (with '#' representing obstacles and '.' representing free cells) to a grid
        """

        self.height = height
        self.width = width
        self._width = self.width
        self._height = self.height
        self._cells = [[0 for _ in range(width)] for _ in range(height)]
        cell_lines = cell_str.split("\n")
        i = 0
        j = 0
        for l in cell_lines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self._cells[i][j] = 0
                    elif c == '#' or c == '@' or c == 'T':
                        self._cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

    def in_bounds(self, i: int, j: int) -> bool:
        """
        Check if the cell is on the grid.
        """
        return (0 <= j < self.width) and (0 <= i < self.height)

    def get_size(self) -> tp.Tuple[int, int]:
        return self.height, self.width

    def is_corner_point(self, i: int, j: int) -> bool:
        cells = self._cells_near_point(i, j)
        return len(cells) == 4 and sum(cells) == 1

    def get_cell(self, i: int, j: int) -> tp.Optional[int]:
        if self.in_bounds(i, j):
            return self._cells[i][j]
        else:
            return None

    def _cells_near_point(self, i: int, j: int) -> tp.List[int]:
        result = []
        for ni in [i - 1, i]:
            for nj in [j - 1, j]:
                cur = self.get_cell(ni, nj)
                if cur is not None:
                    result.append(cur)
        return result

    def is_traversible(self, i: int, j: int) -> bool:
        return any([x == 0 for x in self._cells_near_point(i, j)])

    def is_traversable_edge(self, row: int, col: int, dir: tp.Literal[-1, 1]) -> bool:
        if dir == 1:
            return self.get_cell(row, col) == 0 or self.get_cell(row - 1, col) == 0
        else:
            return self.get_cell(row, col - 1) == 0 or self.get_cell(row - 1, col - 1) == 0

    def is_between_obstacles(self, i: int, j: int) -> bool:
        if self.get_cell(i - 1, j - 1) and self.get_cell(i, j):
            return True
        if self.get_cell(i - 1, j) and self.get_cell(i, j - 1):
            return True
        return False

# start of copy-paste of Andrey's grid methods

    def cell_in_bounds(self, i, j):
        '''
        Check if the cell is on a grid.
        '''
        return (0 <= j < self._width) and (0 <= i < self._height)

    def traversable(self, i, j):
        '''
        Check if the cell is not an obstacle.
        '''
        return self.cell_in_bounds(i, j) and (not self._cells[i][j])

    def visible_axes(self, i1, j1, i2, j2):
        if i1 == i2:
            if j1 > j2:
                j1, j2 = j2, j1
            for j in range(j1, j2):
                if not (self.traversable(i1, j) or self.traversable(i1 - 1, j)):
                    return False
            return True
        if j1 == j2:
            if i1 > i2:
                i1, i2 = i2, i1
            for i in range(i1, i2):
                if not (self.traversable(i, j1) or self.traversable(i, j1 - 1)):
                    return False
            return True
        return False  # this call not allowed

    def visible(self, i1, j1, i2, j2):
        if (i1 == i2) or (j1 == j2):
            return self.visible_axes(i1, j1, i2, j2)

        cells = intersect_cells(i1, j1, i2, j2)
        for cell in cells:
            if not self.traversable(cell[0], cell[1]):
                #                print("invisible : (", i1, ",", j1, ") and (", i2, ",", j2, ")")
                return False
        #        print("  visible : (", i1, ",", j1, ") and (", i2, ",", j2, ")")
        return True


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

# end of copy-paste of Andrey's grid methods

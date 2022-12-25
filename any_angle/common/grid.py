import typing as tp

from .utils import intersect_cells, intersect_points, vect_product


class Map:
    def __init__(self):
        """
        Default constructor
        """

        self._width = 0
        self._height = 0
        self.height = 0
        self.width = 0
        self._cells = []
        self._special_points = set()

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

    def cell_in_bounds(self, i, j):
        """
        Check if the cell is on a grid.
        """
        return (0 <= j < self._width) and (0 <= i < self._height)

    def point_in_bounds(self, i, j):
        """
        Check if the cell is on a grid.
        """
        return (0 <= j <= self._width) and (0 <= i <= self._height)

    def traversable(self, i, j):
        """
        Check if the cell is not an obstacle.
        """
        return self.cell_in_bounds(i, j) and (not self._cells[i][j])

    def not_traversable(self, i, j):
        """
        Check if the cell is not an obstacle.
        """
        return self.cell_in_bounds(i, j) and (self._cells[i][j])

    def passable_point(self, i, j):
        if (not self.traversable(i, j)) and (not self.traversable(i - 1, j - 1)):
            return False
        if (not self.traversable(i, j - 1)) and (not self.traversable(i - 1, j)):
            return False
        return True

    def add_special_point(self, point):
        self._special_points.add(point)

    # return true if we can add this point when expand neighbours
    def stayable_point(self, i, j):
        return self.point_in_bounds(i, j) and (self.passable_point(i, j) or (i, j) in self._special_points)

    def get_blocked_cells(self, i, j):
        cells = []
        delta = [[0, 0], [-1, 0], [0, -1], [-1, -1]]
        for d in delta:
            if self.not_traversable(i + d[0], j + d[1]):
                cells.append((i + d[0], j + d[1]))
        return cells

    def visible_axes(self, i1, j1, i2, j2):
        if i1 == i2:
            if j1 > j2:
                j1, j2 = j2, j1
            for j in range(j1, j2):
                if not (self.traversable(i1, j) or self.traversable(i1 - 1, j)):
                    return False
            for j in range(j1 + 1, j2):
                if not self.passable_point(i1, j):
                    return False
            return True
        if j1 == j2:
            if i1 > i2:
                i1, i2 = i2, i1
            for i in range(i1, i2):
                if not (self.traversable(i, j1) or self.traversable(i, j1 - 1)):
                    return False
            for i in range(i1 + 1, i2):
                if not self.passable_point(i, j1):
                    return False
            return True
        return False  # this call not allowed

    def visible(self, i1, j1, i2, j2):
        if (i1 == i2) or (j1 == j2):
            return self.visible_axes(i1, j1, i2, j2)

        cells = intersect_cells(i1, j1, i2, j2)
        for cell in cells:
            if not self.traversable(cell[0], cell[1]):
                return False

        points = intersect_points(i1, j1, i2, j2)
        for point in points:
            if not self.passable_point(point[0], point[1]):
                return False

        return True

    def node_in_bounds(self, i, j):
        """
        Check if the node is on a grid.
        """
        return (0 <= j <= self._width) and (0 <= i <= self._height)

    def neighbor_cells(self, i, j):
        """
        Returns top left coordinates of all neighboring cells
        (some of them may not belong to the map or may not be traversable).

        Order is clockwise, starting with a (i - 1, j).
        """
        res = []
        for delta_i, delta_j in [(-1, 0), (0, 0), (0, -1), (-1, -1)]:
            res.append((i + delta_i, j + delta_j))
        return res

    def nodes_of_cell(self, i, j):
        """
        Returns all nodes of cell with top left corner (i, j). Order is clockwise, starting with a (i, j).
        """
        res = []
        for delta_i, delta_j in [(0, 0), (0, 1), (1, 1), (1, 0)]:
            res.append((i + delta_i, j + delta_j))
        return res

    def neighbor_obstacles(self, i, j):
        """
        Looks to all cells around the node (i, j) and returns a list with
        flags set to the obstacles.

        Order of cells is clockwise, starting with a cell with top left corner (i - 1, j).

        If cell is not on the map, then we interpret it as an obstacle.
        """
        is_obst = []
        for cell in self.neighbor_cells(i, j):
            is_obst.append((not self.cell_in_bounds(*cell)) or (not self.traversable(*cell)))
        return is_obst

    def diagonal_obstacles(self, i, j):
        """
        Returns True if there are diagonal obstacles around node (i, j). False otherwise.
        """
        is_obst = self.neighbor_obstacles(i, j)
        return is_obst[0] and is_obst[2] or is_obst[1] and is_obst[3]

    def ortogonal_move_is_correct(self, i1, j1, i2, j2):
        """
        Checks if ortogonal move from (i1, j1) to (i2, j2) is correct.

        (i1, j1) should be the node on the map.
        """
        move = (i2 - i1, j2 - j1)
        ortogonal_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        nodes_to_check = self.neighbor_cells(i1, j1)
        node1, node2 = None, None
        for i in range(4):
            if ortogonal_moves[i] == move:
                node1 = nodes_to_check[i]
                node2 = nodes_to_check[(i + 1) % 4]
                break
        return (self.cell_in_bounds(*node1) and self.traversable(*node1)) or (
                self.cell_in_bounds(*node2) and self.traversable(*node2))

    def move_is_correct(self, i1, j1, i2, j2):
        """
        Checks if move from (i1, j1) to (i2, j2) is correct.

        (i1, j1) should be the node on the map.
        """
        if not self.node_in_bounds(i2, j2):
            return False

        if abs(i2 - i1) + abs(j2 - j1) == 1:
            return self.ortogonal_move_is_correct(i1, j1, i2, j2)

        for cell in intersect_cells(i1, j1, i2, j2):
            cell = (cell[0], cell[1])
            if not self.cell_in_bounds(*cell) or self.traversable(*cell):
                continue
            vect_prod_signs = set()
            for node in self.nodes_of_cell(*cell):
                vp = vect_product(node[0] - i1, node[1] - j1, i2 - i1, j2 - j1)
                vect_prod_signs.add(1 if vp > 0 else
                                    -1 if vp < 0 else 0)
            if (1 in vect_prod_signs) and (-1 in vect_prod_signs):
                return False
        return True

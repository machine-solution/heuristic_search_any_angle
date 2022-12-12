from utils import vect_product, scalar_product, intersect_cells


class Map:

    def __init__(self):
        '''
        Default constructor
        '''

        self._width = 0
        self._height = 0
        self._cells = []
        self._delta = []
        self._k = 0

    def read_from_string(self, cell_str, width, height):
        '''
        Converting a string (with '@' representing obstacles and '.' representing free cells) to a grid
        '''
        self._width = width
        self._height = height
        self._cells = [[0 for _ in range(width)] for _ in range(height)]
        cell_lines = cell_str.split("\n")
        i = 0
        for l in cell_lines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self._cells[i][j] = 0
                    elif c == '@' or c == 'T':
                        self._cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

    def set_grid_cells(self, width, height, grid_cells):
        '''
        Initialization of map by list of cells.
        '''
        self._width = width
        self._height = height
        self._cells = grid_cells

    def cell_in_bounds(self, i, j):
        '''
        Check if the cell is on a grid.
        '''
        return (0 <= j < self._width) and (0 <= i < self._height)

    def node_in_bounds(self, i, j):
        '''
        Check if the node is on a grid.
        '''
        return (0 <= j <= self._width) and (0 <= i <= self._height)

    def traversable(self, i, j):
        '''
        Check if the cell is not an obstacle.
        '''
        return not self._cells[i][j]

    def _make_delta(self, k):
        '''
        Generate all directions in clockwise order, starting with (-1, 0).
        '''
        if k == self._k:
            return
        self._k = k
        delta = [(-1, 0), (0, 1)]
        for _ in range(k - 2):
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

    def _neighbor_cells(self, i, j):
        '''
        Returns top left coordinates of all neighboring cells
        (some of them may not belong to the map or may not be traversable).

        Order is clockwise, starting with a (i - 1, j).
        '''
        res = []
        for delta_i, delta_j in [(-1, 0), (0, 0), (0, -1), (-1, -1)]:
            res.append((i + delta_i, j + delta_j))
        return res

    def _nodes_of_cell(self, i, j):
        '''
        Returns all nodes of cell with top left corner (i, j). Order is clockwise, starting with a (i, j).
        '''
        res = []
        for delta_i, delta_j in [(0, 0), (0, 1), (1, 1), (1, 0)]:
            res.append((i + delta_i, j + delta_j))
        return res

    def _neighbor_obstacles(self, i, j):
        '''
        Looks to all cells around the node (i, j) and returns a list with
        flags set to the obstacles.

        Order of cells is clockwise, starting with a cell with top left corner (i - 1, j).

        If cell is not on the map, then we interpret it as an obstacle.
        '''
        is_obst = []
        for cell in self._neighbor_cells(i, j):
            is_obst.append((not self.cell_in_bounds(*cell)) or (not self.traversable(*cell)))
        return is_obst

    def _diagonal_obstacles(self, i, j):
        '''
        Returns True if there are diagonal obstacles around node (i, j). False otherwise.
        '''
        is_obst = self._neighbor_obstacles(i, j)
        return is_obst[0] and is_obst[2] or is_obst[1] and is_obst[3]

    def _ortogonal_move_is_correct(self, i1, j1, i2, j2):
        '''
        Checks if ortogonal move from (i1, j1) to (i2, j2) is correct.

        (i1, j1) should be the node on the map.
        '''
        move = (i2 - i1, j2 - j1)
        ortogonal_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        nodes_to_check = self._neighbor_cells(i1, j1)
        node1, node2 = None, None
        for i in range(4):
            if ortogonal_moves[i] == move:
                node1 = nodes_to_check[i]
                node2 = nodes_to_check[(i + 1) % 4]
                break
        return (self.cell_in_bounds(*node1) and self.traversable(*node1)) or (
                    self.cell_in_bounds(*node2) and self.traversable(*node2))

    def _move_is_correct(self, i1, j1, i2, j2):
        '''
        Checks if move from (i1, j1) to (i2, j2) is correct.

        (i1, j1) should be the node on the map.
        '''
        if not self.node_in_bounds(i2, j2):
            return False

        if abs(i2 - i1) + abs(j2 - j1) == 1:
            return self._ortogonal_move_is_correct(i1, j1, i2, j2)

        for cell in intersect_cells(i1, j1, i2, j2):
            cell = (cell[0], cell[1])
            if self.traversable(*cell):
                continue
            vect_prod_signs = set()
            for node in self._nodes_of_cell(*cell):
                vp = vect_product(node[0] - i1, node[1] - j1, i2 - i1, j2 - j1)
                vect_prod_signs.add(1 if vp > 0 else
                                    -1 if vp < 0 else 0)
            if (1 in vect_prod_signs) and (-1 in vect_prod_signs):
                return False
        return True

    def get_neighbors(self, i, j, k):
        neighbors = []
        self._make_delta(k)
        for d in self._delta:
            if self._move_is_correct(i, j, i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))
        return neighbors

    def get_natural_neighbors(self, i, j, number_of_prev_move, k):
        neighbors = []
        self._make_delta(k)

        if number_of_prev_move is None:
            for ind, d in enumerate(self._delta):
                if self._move_is_correct(i, j, i + d[0], j + d[1]):
                    neighbors.append((i + d[0], j + d[1], ind))
            return neighbors

        if number_of_prev_move % 2:
            for ind in range(-1, 2):
                number_of_current_move = (number_of_prev_move + ind + 2 ** k) % 2 ** k
                d = self._delta[number_of_current_move]
                if self._move_is_correct(i, j, i + d[0], j + d[1]):
                    neighbors.append((i + d[0], j + d[1], number_of_current_move))
        else:
            d = self._delta[number_of_prev_move]
            if self._move_is_correct(i, j, i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1], number_of_prev_move))
        return neighbors

    def get_forced_neighbors(self, i, j, number_of_prev_move, k):
        '''
        Can intersect with natural neighbors by no more then one
        direction but that is doesn't affect algorithm's correctness.
        '''
        if number_of_prev_move is None:
            return []

        if sum(self._neighbor_obstacles(i, j)) != 1:
            return []

        neighbors = []
        self._make_delta(k)
        # next indexes are of ortogonal moves around an obstacle
        m1_ind = -1
        m2_ind = -1
        for ind, cell in enumerate(self._neighbor_cells(i, j)):
            if not self.traversable(*cell):
                m1_ind = ind * 2 ** (k - 2)
                m2_ind = ((ind + 1) % 4) * 2 ** (k - 2)
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
            ind2 += 2 ** k
        for ind in range(ind1, ind2 + 1):
            number_of_current_move = ind % 2 ** k
            d = self._delta[number_of_current_move]
            if self._move_is_correct(i, j, i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1], number_of_current_move))
        return neighbors

    def get_size(self):
        return self._height, self._width

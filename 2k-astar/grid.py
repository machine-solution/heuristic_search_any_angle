from utils import vect_product, intersect_cells


class Node:
    '''
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node
    - F: f-value of the node
    - parent: pointer to the parent-node

    '''

    def __init__(self, i, j, g=0, h=0, f=None, parent=None, tie_breaking_func=None):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        if f is None:
            self.f = self.g + h
        else:
            self.f = f
        self.parent = parent

    def __eq__(self, other):
        '''
        Estimating where the two search nodes are the same,
        which is needed to detect dublicates in the search tree.
        '''
        return (self.i == other.i) and (self.j == other.j)

    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        ij = self.i, self.j
        return hash(ij)

    def __lt__(self, other):
        '''
        Comparing the keys (i.e. the f-values) of two nodes,
        which is needed to sort/extract the best element from OPEN.

        This comparator is very basic. We will code a more plausible comparator further on.
        '''
        return self.f < other.f


class Map:
    def __init__(self):
        '''
        Default constructor
        '''
        self._width = 0
        self._height = 0
        self._cells = []

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

    def neighbor_cells(self, i, j):
        '''
        Returns top left coordinates of all neighboring cells
        (some of them may not belong to the map or may not be traversable).

        Order is clockwise, starting with a (i - 1, j).
        '''
        res = []
        for delta_i, delta_j in [(-1, 0), (0, 0), (0, -1), (-1, -1)]:
            res.append((i + delta_i, j + delta_j))
        return res

    def nodes_of_cell(self, i, j):
        '''
        Returns all nodes of cell with top left corner (i, j). Order is clockwise, starting with a (i, j).
        '''
        res = []
        for delta_i, delta_j in [(0, 0), (0, 1), (1, 1), (1, 0)]:
            res.append((i + delta_i, j + delta_j))
        return res

    def neighbor_obstacles(self, i, j):
        '''
        Looks to all cells around the node (i, j) and returns a list with
        flags set to the obstacles.

        Order of cells is clockwise, starting with a cell with top left corner (i - 1, j).

        If cell is not on the map, then we interpret it as an obstacle.
        '''
        is_obst = []
        for cell in self.neighbor_cells(i, j):
            is_obst.append((not self.cell_in_bounds(*cell)) or (not self.traversable(*cell)))
        return is_obst

    def diagonal_obstacles(self, i, j):
        '''
        Returns True if there are diagonal obstacles around node (i, j). False otherwise.
        '''
        is_obst = self.neighbor_obstacles(i, j)
        return is_obst[0] and is_obst[2] or is_obst[1] and is_obst[3]

    def ortogonal_move_is_correct(self, i1, j1, i2, j2):
        '''
        Checks if ortogonal move from (i1, j1) to (i2, j2) is correct.

        (i1, j1) should be the node on the map.
        '''
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
        '''
        Checks if move from (i1, j1) to (i2, j2) is correct.

        (i1, j1) should be the node on the map.
        '''
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

    def get_size(self):
        return self._height, self._width

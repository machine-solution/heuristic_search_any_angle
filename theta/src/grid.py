
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
        Converting a string (with '@' and 'T' representing obstacles and '.' representing free cells) to a grid
        '''
        self._width = width
        self._height = height
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
                    elif c == '@' or c == 'T':
                        self._cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width )
                
                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height )
    
     
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

    def point_in_bounds(self, i, j):
        '''
        Check if the cell is on a grid.
        '''
        return (0 <= j <= self._width) and (0 <= i <= self._height)
    

    def traversable(self, i, j):
        '''
        Check if the cell is not an obstacle.
        '''
        return self.cell_in_bounds(i, j) and (not self._cells[i][j])
    
    def cells_by_delta(self, di, dj):
        if di == 1 and dj == 0:
            return [[0, 0], [0, -1]]
        if di == -1 and dj == 0:
            return [[-1, 0], [-1, -1]]
        if di == 0 and dj == 1:
            return [[0, 0], [-1, 0]]
        if di == 0 and dj == -1:
            return [[0, -1], [-1, -1]]


    def get_neighbors(self, i, j, k = 8):
        '''
        Get a list of neighbouring cells as (i,j) tuples.
        It's assumed that grid is 8-connected and we can't cut angles
        '''   
        neighbors = []
        if k == 4:
            delta = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        if k == 8:
            delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        if k == 16:
            delta = [[0, 1], [1, 0], [0, -1], [-1, 0],
                     [1, 1], [-1, -1], [1, -1], [-1, 1],
                     [1, 2], [-1, -2], [1, -2], [-1, 2],
                     [2, 1], [-2, -1], [2, -1], [-2, 1]]


        for d in delta:
            if self.point_in_bounds(i + d[0], j + d[1]):
                if self.visible(i, j, i + d[0], j + d[1]):
                    neighbors.append((i + d[0], j + d[1]))

        return neighbors
    
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
        return False # this call not allowed
    
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

    def get_size(self):
        return (self._height, self._width)

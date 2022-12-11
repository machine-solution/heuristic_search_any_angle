import typing as tp


class Map:
    def __init__(self, cell_str: str, width: int, height: int):
        """
        Convert a string (with '#' representing obstacles and '.' representing free cells) to a grid
        """

        self.width = width
        self.height = height
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
                    elif c == '#':
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
        return any(self._cells_near_point(i, j))

    def is_between_obstacles(self, i: int, j: int) -> bool:
        if self.get_cell(i - 1, j - 1) and self.get_cell(i, j):
            return True
        if self.get_cell(i - 1, j) and self.get_cell(i, j - 1):
            return True
        return False

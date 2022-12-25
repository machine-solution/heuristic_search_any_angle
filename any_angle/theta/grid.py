from ..common.grid import Map


class MapTheta(Map):
    def get_neighbors(self, i, j, k=8):
        """
        Get a list of neighbouring cells as (i,j) tuples.
        It's assumed that grid is 8-connected and we can't cut angles
        """
        neighbors = []
        if k == 4:
            delta = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        elif k == 8:
            delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        elif k == 16:
            delta = [[0, 1], [1, 0], [0, -1], [-1, 0],
                     [1, 1], [-1, -1], [1, -1], [-1, 1],
                     [1, 2], [-1, -2], [1, -2], [-1, 2],
                     [2, 1], [-2, -1], [2, -1], [-2, 1]]
        else:
            assert False, "k should be 4, 8 or 16"

        for d in delta:
            if self.stayable_point(i + d[0], j + d[1]):
                if self.visible(i, j, i + d[0], j + d[1]):
                    neighbors.append((i + d[0], j + d[1]))

        return neighbors

class Node:
    """
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node
    - F: f-value of the node
    - parent: pointer to the parent-node

    """

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
        """
        Estimating where the two search nodes are the same,
        which is needed to detect dublicates in the search tree.
        """
        return (self.i == other.i) and (self.j == other.j)

    def __hash__(self):
        """
        To implement CLOSED as set of nodes we need Node to be hashable.
        """
        ij = self.i, self.j
        return hash(ij)

    def __lt__(self, other):
        """
        Comparing the keys (i.e. the f-values) of two nodes,
        which is needed to sort/extract the best element from OPEN.

        This comparator is very basic. We will code a more plausible comparator further on.
        """
        return self.f < other.f

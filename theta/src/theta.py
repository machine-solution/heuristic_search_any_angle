from .utils import compute_cost, Stats, sqr_dist
from .grid import Map

from datetime import datetime
import math

class Node:
    def __init__(self, i, j, g = 0, h = 0, f = None, parent = None):
        self.i = i
        self.j = j
        self.parent = parent
        self.g = g
        self.h = h
        self.true_node = True
        if f is None:
            self.f = self.g + h
        else:
            self.f = f  
        self.tie = math.inf
            
    def apply_heuristic(self, heuristic_func, goal_i, goal_j, w=0.1):
        h = heuristic_func(self, goal_i, goal_j, w)
        if type(h) == tuple:
            self.h = h[0]
            self.tie = h[1]
        else:
            self.h = h
        self.f = self.g + self.h

    
    def __eq__(self, other):
        '''
        Estimating where the two search nodes are the same,
        which is needed to detect dublicates in the search tree.
        '''
        return (self.i == other.i) and (self.j == other.j) # TODO I also want to compare parents 
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        ij = self.i, self.j
        return hash(ij)
    
    # this function defines order of taking nodes from OPEN
    def priority(self):
        return self.f, self.tie, -self.g

    def __lt__(self, other):
        return (self.i, self.j) < (other.i, other.j)
    
    def __le__(self, other):
        return (self.i, self.j) <= (other.i, other.j)
    
    def __gt__(self, other):
        return (self.i, self.j) > (other.i, other.j)
    
    def __ge__(self, other):
        return (self.i, self.j) >= (other.i, other.j)
    
    def __eq__(self, other):
        return (self.i, self.j) == (other.i, other.j)
    
    def __ne__(self, other):
        return (self.i, self.j) != (other.i, other.j)
    

def make_path(goal):
    '''
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    '''
    length = goal.g
    current = goal
    path = []
    while current.parent != current:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length


def getSuccessor(node, i, j, grid_map, goal_i, goal_j, heuristic_func, w):
    if grid_map.visible(node.parent.i, node.parent.j, i, j):
        if sqr_dist(i, j, node.parent.i, node.parent.j) <= sqr_dist(node.i, node.j, node.parent.i, node.parent.j):
            return None
        suc = Node(i, j, g = node.parent.g + compute_cost(node.parent.i, node.parent.j, i, j),
                    parent = node.parent)
        suc.apply_heuristic(heuristic_func, goal_i, goal_j, w)
        return suc
    else:
        suc = Node(i, j, g = node.g + compute_cost(node.i, node.j, i, j),
                    parent = node)
        suc.apply_heuristic(heuristic_func, goal_i, goal_j, w)
        return suc


def getSuccessors(node, grid_map, goal_i, goal_j, heuristic_func, w, p, k):
    neighbors = grid_map.get_neighbors(node.i, node.j, k)
    successors = []
    for cell in neighbors:
        suc = getSuccessor(node, cell[0], cell[1], grid_map, goal_i, goal_j, heuristic_func, w)
        if not (suc is None):
            successors.append(suc)
    return successors


def theta(grid_map: Map, start_i, start_j, goal_i, goal_j, heuristic_func = None, search_tree = None, w = 1, p = 1, k = 8):
    
    start_time = datetime.now() #statistic
    
    stats = Stats() # statistic
    
    grid_map.add_special_point((goal_i, goal_j))

    ast = search_tree() 
    start = Node(start_i, start_j, g=0, parent = None)
    start.parent = start
    start.apply_heuristic(heuristic_func, goal_i, goal_j, w)
    start.parent = start
    ast.add_to_open(start)
    
    while not ast.open_is_empty():
        curr = ast.get_best_node_from_open()
        if curr is None:
            break
            
        ast.add_to_closed(curr)
        
        if (curr.i == goal_i) and (curr.j == goal_j): # curr is goal
            stats.runtime = datetime.now() - start_time # statistic
            stats.way_length = make_path(curr)[1] # statistic
            return  (True, curr, stats, ast.OPEN, ast.CLOSED)
        
        # expanding curr
        stats.expansions += 1 # statistic
        successors = getSuccessors(curr, grid_map, goal_i, goal_j, heuristic_func, w, p, k)
        
        for node in successors:
            ast.add_to_open(node)
                
        stats.max_tree_size = max(stats.max_tree_size, len(ast)) # statistic
        
    stats.runtime = datetime.now() - start_time # statistic
    stats.way_length = 0 # statistic
    return (False, None, stats, ast.OPEN, ast.CLOSED)

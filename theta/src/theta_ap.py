from .utils import compute_cost, Stats, angle_n, dist_n
from .theta import Node, make_path
from .grid import Map

from datetime import datetime
from math import pi
import math

class NodeAP(Node):
    def __init__(self, i, j, g = 0, h = 0, f = None, parent = None, prev = None):
        self.i = i
        self.j = j
        self.parent = parent
        self.prev = prev
        self.g = g
        self.h = h
        self.true_node = True
        if f is None:
            self.f = self.g + h
        else:
            self.f = f  
        self.lb = -pi
        self.ub = pi
        self.tie = math.inf

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


def updateBounds(node: NodeAP, start_i, start_j, grid_map, search_tree, fast = True):
    node.lb = -pi
    node.ub = pi
    if node == NodeAP(start_i, start_j):
        return
    
    delta = [[0, 0], [1, 0], [0, 1], [1, 1]]
    blocked = grid_map.get_blocked_cells(node.i, node.j)
    
    for b in blocked:
        applyL = True
        applyR = True
        for d in delta:
            corner = NodeAP(b[0] + d[0], b[1] + d[1])
            locApplyL = False
            if node.parent == corner:
                locApplyL = True
            if angle_n(node, node.parent, corner) < 0:
                locApplyL = True
            if angle_n(node, node.parent, corner) == 0 and dist_n(node.parent, corner) <= dist_n(node.parent, node): 
                locApplyL = True
            applyL = applyL and locApplyL

            locApplyR = False
            if node.parent == corner:
                locApplyR = True
            if angle_n(node, node.parent, corner) > 0:
                locApplyR = True
            if angle_n(node, node.parent, corner) == 0 and dist_n(node.parent, corner) <= dist_n(node.parent, node): 
                locApplyR = True
            applyR = applyR and locApplyR
        
        if applyL:
            node.lb = 0
        
        if applyR:
            node.ub = 0
    
    sucs = grid_map.get_neighbors(node.i, node.j, k=8)
    for s in sucs:       
        tree_s = None
        if fast:
            if s[0] == node.prev.i and s[1] == node.prev.j:
                tree_s = node.prev
        else:
            tree_s = search_tree.get_if_expanded(NodeAP(s[0], s[1]))
        point_s = NodeAP(s[0], s[1])
        if not (tree_s is None) and node.parent == tree_s.parent and tree_s != NodeAP(start_i, start_j):
            if tree_s.lb + angle_n(node, node.parent, tree_s) <= 0:
                node.lb = max(node.lb, tree_s.lb + angle_n(node, node.parent, tree_s))
            if tree_s.ub + angle_n(node, node.parent, tree_s) >= 0:
                node.ub = min(node.ub, tree_s.ub + angle_n(node, node.parent, tree_s))
        if dist_n(node.parent, point_s) < dist_n(node.parent, node) and node.parent != point_s and (tree_s is None or node.parent != tree_s.parent):
            if angle_n(node, node.parent, point_s) < 0:
                node.lb = max(node.lb, angle_n(node, node.parent, point_s))
            if angle_n(node, node.parent, point_s) > 0:
                node.ub = min(node.ub, angle_n(node, node.parent, point_s))


def getSuccessors(node, grid_map, goal_i, goal_j, heuristic_func, start_i, start_j, search_tree):
    updateBounds(node, start_i, start_j, grid_map, search_tree)
    sucs = grid_map.get_neighbors(node.i, node.j, k=8)
    point_start = NodeAP(start_i, start_j)
    nodes = []
    for suc in sucs:
        snode = NodeAP(suc[0], suc[1], prev=node)
        if point_start != snode and node.lb <= angle_n(node, node.parent, snode) <= node.ub:
            snode.g = node.parent.g + dist_n(node.parent, snode)
            snode.parent = node.parent
            snode.apply_heuristic(heuristic_func, goal_i, goal_j)
            nodes.append(snode)
        else:
            snode.g = node.g + dist_n(node, snode)
            snode.parent = node
            snode.apply_heuristic(heuristic_func, goal_i, goal_j)
            nodes.append(snode)
    return nodes


def theta_ap(grid_map, start_i, start_j, goal_i, goal_j, heuristic_func = None, search_tree = None):
    
    start_time = datetime.now() #statistic
    
    stats = Stats() # statistic

    grid_map.add_special_point((goal_i, goal_j))
    
    ast = search_tree() 
    start = NodeAP(start_i, start_j, g=0, parent = None)
    start.parent = start
    start.prev = start
    start.apply_heuristic(heuristic_func, goal_i, goal_j)
    start.parent = start
    ast.add_to_open(start)
    
    while not ast.open_is_empty():
        curr = ast.get_best_node_from_open()
        if curr is None:
            break
            
        ast.add_to_closed(curr)

#        print("(", curr.parent.i, ",", curr.parent.j, ") --> (", curr.i, ",", curr.j, ")  <", curr.lb, ",", curr.ub, ">")
        
        if (curr.i == goal_i) and (curr.j == goal_j): # curr is goal
            stats.runtime = datetime.now() - start_time # statistic
            stats.way_length = make_path(curr)[1] # statistic
            return  (True, curr, stats, ast.OPEN, ast.CLOSED)
        
        # expanding curr
#        print(curr.i, curr.j, "prev", curr.prev.i, curr.prev.j, "parent", curr.parent.i, curr.parent.j)
        stats.expansions += 1 # statistic
        successors = getSuccessors(curr, grid_map, goal_i, goal_j, heuristic_func, start_i, start_j, ast)
        
        for node in successors:
            if not ast.was_expanded(node):
                ast.add_to_open(node)
                
        stats.max_tree_size = max(stats.max_tree_size, len(ast)) # statistic
        
    stats.runtime = datetime.now() - start_time # statistic
    stats.way_length = 0 # statistic
    return (False, None, stats, ast.OPEN, ast.CLOSED)

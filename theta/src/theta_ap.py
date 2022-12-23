from .utils import compute_cost_n, Stats, sqr_dist_n, Vector, Point
from .theta import Node, make_path
from .grid import Map

from datetime import datetime
from math import pi
import math

class NodeAP(Node):
    def __init__(self, i, j, g = 0, h = 0, f = None, parent = None, prev = None):
        self.i = i
        self.j = j
        if parent is None:
            self.parent = self
        else:
            self.parent = parent
        if prev is None:
            self.prev = self
        else:
            self.prev = prev
        self.g = g
        self.h = h
        self.true_node = True
        if f is None:
            self.f = self.g + h
        else:
            self.f = f 
        self.lv = Vector(self.parent.i - self.i, self.parent.j - self.j)
        self.uv = Vector(self.parent.i - self.i, self.parent.j - self.j)
        self.straight = Vector(self.i - self.parent.i, self.j - self.parent.j)
        self.tie = math.inf

    def __repr__(self):
        return str(self.i) + ", " + str(self.j)


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


def updateBounds(node: NodeAP, start_i, start_j, grid_map, search_tree):
    # print("update bounds node ", node.i, node.j)
    # print("prev", node.prev.i, node.prev.j, "parent", node.parent.i, node.parent.j)
    if node == Point(start_i, start_j):
        # print("Updated: ", node.i, node.j, "lv: ", node.lv, " uv: ", node.uv )
        return
    
    delta = [[0, 0], [1, 0], [0, 1], [1, 1]]
    blocked = grid_map.get_blocked_cells(node.i, node.j)
    
    for b in blocked:
        applyL = True
        applyU = True
        for d in delta:
            corner = Point(b[0] + d[0], b[1] + d[1])
            vcorner = Vector(corner.i - node.parent.i, corner.j - node.parent.j)
            locApplyU = False
            if node.parent == corner:
                locApplyU = True
            if node.straight < vcorner:
                locApplyU = True
            if node.straight == vcorner and sqr_dist_n(node.parent, corner) <= sqr_dist_n(node.parent, node): 
                locApplyU = True
            applyU = applyU and locApplyU

            locApplyL = False
            if node.parent == corner:
                locApplyL = True
            if node.straight > vcorner:
                locApplyL = True
            if node.straight == vcorner and sqr_dist_n(node.parent, corner) <= sqr_dist_n(node.parent, node): 
                locApplyL = True
            applyL = applyL and locApplyL
        
        if applyL:
            node.lv = node.straight
            # print("low vector by cell ", b, "to", node.lv)
        
        if applyU:
            node.uv = node.straight
            # print("up  vector by cell ", b, "to", node.uv)
    
    sucs = grid_map.get_neighbors(node.i, node.j, k=8)
    for s in sucs:       
        tree_s = None
        if s[0] == node.prev.i and s[1] == node.prev.j:
            tree_s = node.prev

        point_s = Point(s[0], s[1])
        vector_s = Vector(s[0] - node.parent.i, s[1] - node.parent.j)
        if not (tree_s is None) and node.parent == tree_s.parent and tree_s != Point(start_i, start_j):
            # print("prev bounds", "lv", tree_s.lv, "uv", tree_s.uv)
            if tree_s.lv <= node.straight:
                if tree_s.lv >= node.lv:
                    node.lv = tree_s.lv
                # print("low vector by prev ", point_s, "to", node.lv)
            # else:
            #     node.lv = node.straight
            if tree_s.uv >= node.straight:
                node.uv = min(node.uv, tree_s.uv)
                if tree_s.uv <= node.uv:
                    node.uv = tree_s.uv
                # print("up  vector by prev ", point_s, "to", node.uv)
            # else:
            #     node.uv = node.straight
        if node.parent != point_s and (tree_s is None or node.parent != tree_s.parent) and sqr_dist_n(node.parent, point_s) < sqr_dist_n(node.parent, node):
            if vector_s < node.straight:
                if vector_s >= node.lv:
                    node.lv = vector_s
                # print("low vector by point ", point_s, "to", node.lv)
            if vector_s > node.straight:
                if vector_s <= node.uv:
                    node.uv = vector_s
                # print("up  vector by point ", point_s, "to", node.uv)

    # print("Updated: ", node.i, node.j, "lv: ", node.lv, " uv: ", node.uv )
    return


def getSuccessors(node, grid_map, goal_i, goal_j, heuristic_func, start_i, start_j, search_tree):
    updateBounds(node, start_i, start_j, grid_map, search_tree)
    sucs = grid_map.get_neighbors(node.i, node.j, k=8)
    point_start = Point(start_i, start_j)
    nodes = []
    for suc in sucs:
        spoint = Point(suc[0], suc[1])
        svector = Vector(suc[0] - node.parent.i, suc[1] - node.parent.j)
        # print(spoint, " : ", node.lv, svector, node.uv)
        if point_start != spoint and (node.lv <= svector <= node.straight or node.straight <= svector <= node.uv):
            # print("  visible")
            if sqr_dist_n(spoint, node.parent) <= sqr_dist_n(node, node.parent):
                continue
            snode = NodeAP(suc[0], suc[1], g=node.parent.g + compute_cost_n(node.parent, spoint),
            parent=node.parent, prev=node)
            snode.apply_heuristic(heuristic_func, goal_i, goal_j)
            nodes.append(snode)
        else:
            # print("invisible")
            snode = NodeAP(suc[0], suc[1], g=node.g + compute_cost_n(node, spoint),
            parent=node, prev=node)
            snode.apply_heuristic(heuristic_func, goal_i, goal_j)
            nodes.append(snode)
    return nodes


def theta_ap(grid_map, start_i, start_j, goal_i, goal_j, heuristic_func = None, search_tree = None):
    start_time = datetime.now() #statistic
    
    stats = Stats() # statistic

    grid_map.add_special_point((goal_i, goal_j))
    
    ast = search_tree() 
    start = NodeAP(start_i, start_j, g=0, parent = None, prev = None)
    start.apply_heuristic(heuristic_func, goal_i, goal_j)
    ast.add_to_open(start)
    
    while not ast.open_is_empty():
        curr = ast.get_best_node_from_open()
        if curr is None:
            break
        
        ast.add_to_closed(curr)

        # print("get", curr, "prev", curr.prev, "parent", curr.parent)
        
        if (curr.i == goal_i) and (curr.j == goal_j): # curr is goal
            stats.runtime = datetime.now() - start_time # statistic
            stats.way_length = make_path(curr)[1] # statistic
            return  (True, curr, stats, ast.OPEN, ast.CLOSED)
        
        # expanding curr
        stats.expansions += 1 # statistic
        successors = getSuccessors(curr, grid_map, goal_i, goal_j, heuristic_func, start_i, start_j, ast)
        
        for node in successors:
            if not ast.was_expanded(node):
                ast.add_to_open(node)
                
        stats.max_tree_size = max(stats.max_tree_size, len(ast)) # statistic
        
    stats.runtime = datetime.now() - start_time # statistic
    stats.way_length = 0 # statistic
    return (False, None, stats, ast.OPEN, ast.CLOSED)

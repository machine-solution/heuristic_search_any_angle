from heapq import heappop, heappush

class SearchTreePQS: #SearchTree which uses PriorityQueue for OPEN and set for CLOSED
    
    def __init__(self):
        self._open = [] # priority queue (node.priority, node)
        self._closed = set()
        
    def __len__(self):
        return len(self._open) + len(self._closed)
    
    '''
    open_is_empty should inform whether the OPEN is exhausted or not.
    In the former case the search main loop should be interrupted.
    '''
    def open_is_empty(self):
        return len(self._open) == 0
    
    '''
    Adding a node to the search-tree (i.e. to OPEN).
    It's may be a duplicate, and it will be checked in 
    'get_best_node_from_open' method
    '''    
    def add_to_open(self, item):
        heappush(self._open, (item.priority(), item))
    
    
    '''
    Extracting the best node (i.e. the one with the minimal key 
    = min f-value = min g-value (for Dijkstra)) from OPEN.
    This node will be expanded further on in the main loop of the search.
    Can't return a duplicate.
    return Null if open consist of ONLY closed nodes.
    ''' 
    def get_best_node_from_open(self):
        while not self.open_is_empty():
            bestf, best = heappop(self._open)
            if not (self.was_expanded(best)):
                return best
        return None

    def add_to_closed(self, item):
        self._closed.add(item)

    def was_expanded(self, item):
        return item in self._closed

    @property
    def OPEN(self):
        return [item[1] for item in self._open]
    
    @property
    def CLOSED(self):
        return self._closed


class SearchTreePQS_SDD(SearchTreePQS): #SearchTree which uses PriorityQueue for OPEN and set for CLOSED with semi-detection duplicates
    
    def __init__(self):
        self._open = [] # priority queue (node.priority, node)
        self._closed = set()
        self._best = dict()
        
    def __len__(self):
        return len(self._open) + len(self._closed) + len(self._best)
    
    '''
    Adding a node to the search-tree (i.e. to OPEN).
    It's may be a duplicate, and it will be checked in 
    'get_best_node_from_open' method
    '''    
    def add_to_open(self, item):
        if (self._best.get(item) is None) or (self._best.get(item) > item.g):
            heappush(self._open, (item.priority(), item))
            self._best[item] = item.g

    def add_to_closed(self, item):
        self._closed.add(item)
        self._best[item] = -1 # we can't add it to open anymore


class SearchTreePQSReexp(SearchTreePQS): #SearchTree with reexpansion which uses PriorityQueue for OPEN and set for CLOSED
    
    def __init__(self):
        self._open = [] # priority queue (node.priority, node)
        self._closed = set()
        self._best = dict()
        
    def __len__(self):
        return len(self._open) + len(self._closed) + len(self._best)
    
    '''
    Adding a node to the search-tree (i.e. to OPEN) if f-value was decreased
    It's may be a duplicate, it is norm for this type of tree
    '''    
    def add_to_open(self, item):
        if (self._best.get(item) is None) or (self._best.get(item) > item.g):
            heappush(self._open, (item.priority(), item))
            self._best[item] = item.g
        self._closed.discard(item) # trying to remove without any exceptions


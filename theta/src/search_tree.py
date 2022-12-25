from heapq import heappop, heappush

class SearchTreePQS: #SearchTree which uses PriorityQueue for OPEN and set for CLOSED
    
    def __init__(self):
        self._open = [] # priority queue (node.priority, node)
        self._closed = set()
        
    def __len__(self):
        return len(self._open) + len(self._closed)
    
    def open_is_empty(self):
        return len(self._open) == 0
     
    def add_to_open(self, item):
        heappush(self._open, (item.priority(), item))

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
        return len(self._open) + len(self._closed)
  
    def add_to_open(self, item):
        if (self._best.get(item) is None) or (self._best.get(item) > item.g):
            heappush(self._open, (item.priority(), item))
            self._best[item] = item.g

    def add_to_closed(self, item):
        self._closed.add(item)
        self._best[item] = -1 # we can't add it to open anymore


class SearchTreePQSReexp: #SearchTree with reexpansion which uses PriorityQueue for OPEN and set for CLOSED
    
    def __init__(self):
        self._open = [] # priority queue (node.priority, node)
        self._closed = set()
        self._best = dict()
        
    def __len__(self):
        return len(self._open) + len(self._closed)
    
    def open_is_empty(self):
        return len(self._open) == 0
      
    def add_to_open(self, item):
        if (self._best.get(item) is None) or (self._best.get(item) > item.g):
            heappush(self._open, (item.priority(), item))
            if item.true_node:
                self._best[item] = item.g
        self._closed.discard(item) # trying to remove without any exceptions
    
    def get_best_node_from_open(self):
        if not self.open_is_empty():
            bestf, best = heappop(self._open)
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

#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 01 - Programming Assignment
#
#   2017-07-16
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from string import rstrip
from heapq import heappush

class Graph():
    """Document Graph Class"""
    
    # Default edge weight when not specified
    DefaultWeight = 1
    
    # Shorthand for infinity
    Inf = float('inf')
    
    def __init__(self, directed = False, edges = None):
        """Document Graph Class initializer"""
        self._nodes = defaultdict(
            lambda: {'edgesAtHead': [], 'edgesAtTail': [], 'heapPosition': None}
        )
        self._directed = directed
        self._edges = []
        self._heap = []
        
        # Add edges if not none
        if edges is not None: self.addEdgesFromIterable(edges)

    def __siftdown(self, startPos, pos):
        """Document Graph Class siftdown"""
        while pos > startPos:
            parentPos = (pos - 1) >> 1
            child = self._heap[pos]
            print child
            parent = self._heap[parentPos]
            print parent
            
            # Compare first tuple value and swap if child less than parent
            if child[0] < parent[0]:
                self._heap[parentPos] = child
                self._nodes[child[1]]['heapPosition'] = parentPos
                self._heap[pos] = parent
                self._nodes[parent[1]]['heapPosition'] = pos
            
            # End sift if child's first tuple is greater than or equal to parent
            else: break
        
    def __heappush(self, nodeTuple):
        """Document Graph Class heappush"""
        heapPos = len(self._heap)
        self._heap.append(nodeTuple)
        self._nodes[nodeTuple[1]]['heapPosition'] = heapPos
        self.__siftdown(0, heapPos)
    
    
    def addEdge(self, tail, head, weight = None):
        """Document Graph Class addEdge"""
    
        # Set edge weight to default if None
        weight = self.DefaultWeight if weight is None else weight
        
        # Get new edge position and add to edges
        i = self.getEdgeCount()
        self._edges.append([tail, head, weight])
        
        # Update node edge pointers (directed)
        self._nodes[head]['edgesAtHead'].append(i)
        self._nodes[tail]['edgesAtTail'].append(i)

        # Update node edge pointers (undirected)
        if not(self._directed):
            self._nodes[head]['edgesAtTail'].append(i)
            self._nodes[tail]['edgesAtHead'].append(i)
        
        # Add to head and tail to heap if new
        if self._nodes[head]['heapPosition'] is None:
            self.__heappush((self.Inf, hash(head)))
        if self._nodes[tail]['heapPosition'] is None:
            self.__heappush((self.Inf, hash(tail)))
    
    def addEdgesFromIterable(self, edges):
        """Document Graph Class addEdgesFromList"""
        # Iterate through edges adding each to graph
        for edge in edges:
            self.addEdge(edge[0], edge[1], edge[2] if len(edge) > 2 else None)
    
    def getEdgeCount(self):
        """Document Graph Class getEdgeCount method"""
        return len(self._edges)


#
#   Main
#
# Create undirected graph
g = Graph()

# Open file, set delimeters, and set directed-ness
f = open('Test01.txt', 'r')
edgeDelim = '\t'
attrDelim = ','

# Populate graph from edges in file
for line in list(f):
    # Split line on delimeter and set tail node 
    edges = rstrip(line, edgeDelim + '\r\n').split(edgeDelim)
    tail = int(edges.pop(0))
    
    # Add each edge
    for e in edges:
        split = e.split(attrDelim)
        g.addEdge(tail, int(split[0]), int(split[1]))

print g._edges
print g._nodes
print g._heap
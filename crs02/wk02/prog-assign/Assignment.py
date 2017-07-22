#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 02 - Programming Assignment
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
    # Inf = float('inf') # Use for actual implementation
    Inf = 1000000 # Use for programming assignment
    
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

    def __swapNodesInHeap(self, posA, posB):
        """Document Graph Class swapNodesInHeap method"""
        nodeTupleA = self._heap[posA]
        nodeTupleB = self._heap[posB]
        self._heap[posB] = nodeTupleA
        self._heap[posA] = nodeTupleB
        self._nodes[nodeTupleA[1]]['heapPosition'] = posB
        self._nodes[nodeTupleB[1]]['heapPosition'] = posA

    def __siftup(self, pos, stopPos):
        """Document Graph Class siftup method"""
        while pos > stopPos:
            parentPos = (pos - 1) >> 1

            # Compare first tuple value and swap if child less than parent
            if self._heap[pos][0] < self._heap[parentPos][0]:
                self.__swapNodesInHeap(pos, parentPos)
                pos = parentPos
            
            # End sift if child's first tuple is greater than or equal to parent
            else: break
    
    def __siftdown(self, pos, lastPos = None):
        """Document Graph Class siftdown method"""
        lastPos = lastPos if not None else len(self._heap) - 1
        while pos < lastPos:
            rightChildPos = (pos + 1) << 1
            leftChildPos = rightChildPos - 1

            # Stop if no children
            if(leftChildPos > lastPos): break
        
            # Check left child only if right does not exist
            elif(rightChildPos > lastPos):
                if self._heap[pos][0] > self._heap[leftChildPos][0]:
                    self.__swapNodesInHeap(pos, leftChildPos)
                    pos = leftChildPos
                else: break
            
            # Check both children and swap with lesser
            else:
                if self._heap[leftChildPos][0] <= self._heap[rightChildPos][0]:
                    if self._heap[pos][0] > self._heap[leftChildPos][0]:
                        self.__swapNodesInHeap(pos, leftChildPos)
                        pos = leftChildPos
                        continue
                    elif self._heap[pos][0] > self._heap[rightChildPos][0]:
                        self.__swapNodesInHeap(pos, rightChildPos)
                        pos = rightChildPos
                    else: break
                else:
                    if self._heap[pos][0] > self._heap[rightChildPos][0]:
                        self.__swapNodesInHeap(pos, rightChildPos)
                        pos = rightChildPos
                        continue
                    elif self._heap[pos][0] > self._heap[leftChildPos][0]:
                        self.__swapNodesInHeap(pos, leftChildPos)
                        pos = leftChildPos
                    else: break
        
    def __heappush(self, nodeTuple):
        """Document Graph Class heappush method"""
        heapPos = len(self._heap)
        self._heap.append(nodeTuple)
        self._nodes[nodeTuple[1]]['heapPosition'] = heapPos
        self.__siftup(heapPos, 0)
    
    def __heappop(self, pos = 0, lastPos = None):
        """Document Graph Class heappop method"""
        nodeTuple = self._heap[pos]
        lastPos = lastPos if not None else len(self._heap) - 1
            
        # Move last node into position and sift down
        self._heap[pos] = self._heap.pop(lastPos)
        self._nodes[self._heap[pos][1]]['heapPosition'] = pos
        self.__siftdown(pos, lastPos)
    
        # Return popped node tuple
        return nodeTuple
        
    def addEdge(self, tail, head, weight = None):
        """Document Graph Class addEdge method"""
    
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

    def minPathLengthsFrom(self, node):
        """Document Graph Class minPathLengthsFrom method"""
        minPaths = defaultdict(lambda: None)
        
        # Prepare min-heap by swapping starting node to index zero with path
        # length zero
        self.__swapNodesInHeap(0, self._nodes[hash(node)]['heapPosition'])
        self._heap[0] = (0, self._heap[0][1])
        
        # Loop through nodes
        for lastPos in xrange(len(self._heap)-1, -1, -1):
            # Pop minimum node
            minNode = self.__heappop(0, lastPos)
            
            # Add to minimum path
            minPaths[minNode[1]] = minNode[0]
            
            # Set path length to infinity and return to end of heap
            self.__heappush((self.Inf, minNode[1]))
            # print 'After pop, before re-calc:', self._heap[:lastPos]

            # For nodes in heap reachable from the popped node, set heap sort
            # value to path length from popped node if less than current
            for i in self._nodes[minNode[1]]['edgesAtTail']:
                edge = self._edges[i]
                if minPaths[edge[1]] is not None: continue
                
                heapPos = self._nodes[edge[1]]['heapPosition']
                newPathLen = minNode[0] + edge[2]
                currMinPathLen = self._heap[heapPos][0]
                if newPathLen < currMinPathLen:
                    self._heap[heapPos] = (newPathLen, edge[1])
                    self.__siftup(heapPos, 0)
            
            # print 'After pop and re-calc:', self._heap[:lastPos]

        # Return minimum paths
        return minPaths

#
#   Main
#
# Create undirected graph
g = Graph()

# Open file, set delimeters, and set directed-ness
f = open('dijkstraData.txt', 'r')
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

minPathsFrom1 = g.minPathLengthsFrom(1)

# Use for small test sets
# print minPathsFrom1

# Use for ranom test sets; selects nodes specified by assignment
keys = [7,37,59,82,99,115,133,165,188,197]
for k in keys:
    print k, ':', minPathsFrom1[k]
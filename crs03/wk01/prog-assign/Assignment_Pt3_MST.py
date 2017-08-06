#   Stanford Algorithms Specialization on Coursera
#   Course 03
#   Week 01 - Programming Assignment - Part 3: Minimum Spanning Tree
#
#   2017-08-05
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from heapq import heappush, heapify
from collections import defaultdict
from random import randrange

class MSTGraph (object):
    """Graph for quickly calculating minimum spanning tree.
    
    """
    
    DefaultWeight = 1
    """int: Default edge weight when not specified."""
    
    Inf = float('inf')
    """float: Shorthand for infinity."""
    
    def __init__(self, directed = False, edges = None):
        """Initialize graph.
        
        Args:
            directed (bool, optional): Indicator if the graph is directed.
                Defaults to False (undirected).
            edges (:obj:`list` of :obj:`list`, optional): List of edges in
                format [head, tail, weight]. Weight is optional.
        """
        self.__nodes = defaultdict(
            lambda: {"edgesAtHead":[], "edgesAtTail":[], "heapPosition":None}
        )
        self.__edges = []
        self.__heap = []
        self.__directed = directed
        if edges is not None: self.addEdgeList(edges)

    @property
    def directed(self):
        """bool: Indicator of the graph having directed edges."""
        return self.__directed
    
    @property
    def edgeCount(self):
        """int: Number of edges in the graph."""
        return len(self.__edges)
    
    @property
    def nodeCount(self):
        """int: Number of nodes in the graph."""
        return len(self.__nodes)
    
    def __swapNodesInHeap(self, posA, posB):
        """Swap position of two nodes in heap.
        
        Args:
            posA (int): Index of node A in heap.
            posB (int): Index of node B in heap.
        """
        nodeA = self.__heap[posA]
        nodeB = self.__heap[posB]
        self.__heap[posB] = nodeA
        self.__heap[posA] = nodeB
        self.__nodes[nodeA[1]]['heapPosition'] = posB
        self.__nodes[nodeB[1]]['heapPosition'] = posA

    def __siftup(self, pos, stopPos = 0):
        """Sift node at specified position up until either in correct position
            or at stop position.
            
        Args:
            pos (int): Index of node to sift up.
            stopPos (int, optional): Minimum index at which to stop if reached
                by node. Defaults to zero (0).
        """
        while pos > stopPos:
            # Determine parent position
            parentPos = (pos - 1) >> 1

            # Swap target node with parent if value less parent value.
            if self.__heap[pos][0] < self.__heap[parentPos][0]:
                self.__swapNodesInHeap(pos, parentPos)
                pos = parentPos
            
            # End sift up if target node value greater than or equal to parent.
            else: break
    
    def __siftdown(self, pos, stopPos = None):
        """Sift node at specified position down until either in correct position
            or at stop position.
            
        Args:
            pos (int): Index of node to sift up.
            stopPos (int, optional): Maximum index at which to stop if reached
                by node. Defaults to last position in the heap.
        """
        stopPos = stopPos if stopPos is not None else len(self.__heap) - 1
        while pos < stopPos:
            # Determine child positions
            rightChildPos = (pos + 1) << 1
            leftChildPos = rightChildPos - 1

            # Stop if no children
            if(leftChildPos > stopPos): break
        
            # Check left child only if right does not exist. Swap target node
            # if value greater than left child value.
            elif(rightChildPos > stopPos):
                if self.__heap[pos][0] > self.__heap[leftChildPos][0]:
                    self.__swapNodesInHeap(pos, leftChildPos)
                    pos = leftChildPos
                else: break
            
            # Check both children if both exist. Determine which child, if 
            # either, has lesser value than target and swap with minimum child.
            else:
                minOfThree = [
                    (self.__heap[pos][0], pos),
                    (self.__heap[leftChildPos][0], leftChildPos),
                    (self.__heap[rightChildPos][0], rightChildPos)
                ]
                heapify(minOfThree)

                # Break if parent is minimum
                if minOfThree[0][1] == pos: break
                
                # Else swap with minimum child
                else:
                    self.__swapNodesInHeap(pos, minOfThree[0][1])
                    pos = minOfThree[0][1]
        
    def __heappush(self, hNode):
        """Add node to heap, set its initial back pointer, then sift up.
        
        Args:
            hNode(:obj:`list`): The heap node to add.
        """
        heapPos = len(self.__heap)
        self.__heap.append(hNode)
        self.__nodes[hNode[1]]['heapPosition'] = heapPos
        self.__siftup(heapPos)
    
    def __heappop(self, pos = 0, stopPos = None):
        """Remove node from specified position then restore heap.
        
        Args:
            pos (int, optional): Index of node to remove. Defaults to root.
            stopPos (int, optional): Maximum index at which to stop if reached
                during restore process. Defaults to last position in the heap.
        
        Returns:
            :obj:`list`: Node from heap.
        """
        hNode = self.__heap[pos]
        stopPos = stopPos if stopPos is not None else len(self.__heap) - 1
            
        # Move last node into position and sift down
        self.__heap[pos] = self.__heap.pop(stopPos)
        self.__nodes[self.__heap[pos][1]]['heapPosition'] = pos
        self.__siftdown(pos, stopPos - 1)
    
        # Return popped node tuple
        return hNode
        
    def __recalcHeap(self, nodeKey, lastPos = None):
        """Recalculate heap based on edges now reachable by popped node.
        
        Args:
            nodeKey(str): Popped node key.
            lastPos(int): Last position within heap for un-spanned nodes.
        """
        lastPos = lastPos if lastPos is not None else len(self.__heap) - 1
        for i in self.__nodes[nodeKey]['edgesAtTail']:
            e = self.__edges[i]
            tailNodeKey = e[1] if e[0] == nodeKey else e[0]
            pos = self.__nodes[tailNodeKey]['heapPosition']

            # Continue if edge tail node in MST
            if pos > lastPos: continue
        
            # Continue if edge weight greater than or equal to current minimum
            # edge weight for tail nodes
            if e[2] >= self.__heap[pos][0]: continue
        
            # Else, update minimum edge weight of tail node and sift up.
            self.__heap[pos] = (e[2], tailNodeKey, i)
            self.__siftup(pos)
        
    def addEdge(self, tail, head, weight = None):
        """Add a single edge to the graph. Creates necessary nodes if missing.
        
        Args:
            tail (object): The tail node of the new edge.
            head (object): The head node of the new edge.
            weight (int, optional): The weight of the edge. Defaults to class
                property DefaultWeight.
        """
        weight = self.DefaultWeight if weight is None else weight
        
        # Get new edge position and add to edges
        i = self.edgeCount
        self.__edges.append([tail, head, weight])
        
        # Update node edge pointers (directed)
        self.__nodes[head]['edgesAtHead'].append(i)
        self.__nodes[tail]['edgesAtTail'].append(i)

        # Update node edge pointers (undirected)
        if not(self.directed):
            self.__nodes[head]['edgesAtTail'].append(i)
            self.__nodes[tail]['edgesAtHead'].append(i)
        
        # Add head and tail to heap if new
        if self.__nodes[head]['heapPosition'] is None:
            self.__heappush((self.Inf, head, None))
        if self.__nodes[tail]['heapPosition'] is None:
            self.__heappush((self.Inf, tail, None))
    
    def addEdgeList(self, edges):
        """Add multiple edges from a list.
        
        Args:
            edges (:obj:`list` of :obj:`list`): List of edges in format [head,
                tail, weight]. Weight is optional.
        """
        for e in edges:
            self.addEdge(e[0], e[1], e[2] if len(e) > 2 else None)

    def findMST(self):
        """Return a minimum spanning tree. Picks starting node at random so 
            possible to return different results if multiple MSTs.
        
        Returns:
            :obj:defaultdict: Nodes as keys and values as minimum edge lengths.
            int: Sum of all minimum edge legths.
        """
        mst = {}
        mstTot = 0
        
        # Pop random node to start, return to end with reset minimum edge, then
        # recalcuate heap
        hNode = self.__heappop(0)#randrange(self.nodeCount))
        self.__heappush((self.Inf, hNode[1], None))
        self.__recalcHeap(hNode[1], self.nodeCount - 2)
        
        # Loop through nodes, pop node with minimum edge length, add edge
        # to MST, then return to end of heap.
        for lastPos in xrange(self.nodeCount - 2, -1, -1):
            # print self.__heap[:lastPos + 1], self.__heap[lastPos + 1:]
            hNode = self.__heappop(0, lastPos)
            
            # Add edge to minimum spanning tree
            mst[hNode[2]] = hNode[0]
            mstTot = mstTot + hNode[0]
            
            # Return node to end
            self.__heappush((self.Inf, hNode[1], None))

            # Recalculate heap
            self.__recalcHeap(hNode[1], lastPos - 1)

        # Return minimum spanning tree and sum of minimum edge weights
        return mst, mstTot

#
#   Main
#
# Instantiate MST graph
g = MSTGraph()

# Read jobs from jile
with open('edges.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add edge from each line
    for l in f:
        e = l.strip().split(" ")
        g.addEdge(int(e[0]), int(e[1]), int(e[2]))

# Print graph properties
print "Graph with", g.nodeCount, "nodes and", g.edgeCount, "edges."
mst, mstTot = g.findMST()
# print mst
print len(mst)
print mstTot
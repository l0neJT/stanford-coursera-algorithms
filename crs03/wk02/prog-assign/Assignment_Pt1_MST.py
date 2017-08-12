#   Stanford Algorithms Specialization on Coursera
#   Course 03
#   Week 02 - Programming Assignment - Part 1: Kruskal's Minimum Spanning Tree
#
#   2017-08-012
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from sortedcontainers import SortedListWithKey
from random import randrange

class kMSTGraph (object):
    """Graph for quickly calculating minimum spanning tree using Kruskal's
        algorithm.
    
    """
    
    DefaultWeight = 1
    """int: Default edge weight when not specified."""
    
    Inf = float('inf')
    """float: Shorthand for infinity."""
    
    def __init__(self, edges = None):
        """Initialize graph.
        
        Args:
            edges (:obj:`list` of :obj:`list`, optional): List of edges in
                format [head, tail, weight]. Weight is optional.
        """
        self.__nodes = defaultdict(lambda: None)
        self.__edges = SortedListWithKey(key = lambda e: e[2])
        if edges is not None: self.addEdgeList(edges)

    @property
    def edgeCount(self):
        """int: Number of edges in the graph."""
        return len(self.__edges)
    
    @property
    def nodeCount(self):
        """int: Number of nodes in the graph."""
        return len(self.__nodes)

    def addEdge(self, tail, head, weight = None):
        """Add a single edge to the graph. Creates necessary nodes if missing.
        
        Args:
            tail (object): The tail node of the new edge.
            head (object): The head node of the new edge.
            weight (int, optional): The weight of the edge. Defaults to class
                property DefaultWeight.
        """
        weight = self.DefaultWeight if weight is None else weight
        
        # Add edge
        self.__edges.add([tail, head, weight])
        
        # Add nodes
        self.__nodes[head] = None
        self.__nodes[tail] = None
    
    def addEdgeList(self, edges):
        """Add multiple edges from a list.
        
        Args:
            edges (:obj:`list` of :obj:`list`): List of edges in format [head,
                tail, weight]. Weight is optional.
        """
        for e in edges:
            self.addEdge(e[0], e[1], e[2] if len(e) > 2 else None)

    def findMST(self):
        """Return a minimum spanning tree.

        Returns:
            :obj:`list` of :obj:`list`: List of edges in the MST in the format
                [tail, head, weight].
            int: Sum of all minimum edge legths.
        """
        mst = []
        mstTot = 0
        partitions = []
        
        # Set all node partition indices to None
        for k in self.__nodes.iterkeys():
            self.__nodes[k] = None
        
        # Iterate through edges from smallest to largest adding those that
        # do not create a cycle to the MST
        for e in self.__edges:
            addEdge = False
            tailPartitionIndex = self.__nodes[e[0]]
            headPartitionIndex = self.__nodes[e[1]]
            
            # Add edge to MST and set tail as partition if neither tail nor head
            # previously seen
            if tailPartitionIndex is None and headPartitionIndex is None:
                addEdge = True
                pIndex = len(partitions)
                partitions.append(e[0])
                self.__nodes[e[0]] = pIndex
                self.__nodes[e[1]] = pIndex
            
            # Add edge to MST and copy tail partition index to head if head not
            # previously seen
            elif headPartitionIndex is None:
                addEdge = True
                self.__nodes[e[1]] = tailPartitionIndex
            
            # Add edge to MST and copy head partition index to tail if tail not
            # previously seen
            elif tailPartitionIndex is None:
                addEdge = True
                self.__nodes[e[0]] = headPartitionIndex
                
            # Add edge to MST and merge head partition into tail if not cycle
            elif partitions[headPartitionIndex] != partitions[tailPartitionIndex]:
                addEdge = True
                partitions[headPartitionIndex] = partitions[tailPartitionIndex]
            
            if addEdge:
                mst.append(e)
                mstTot = mstTot + e[2]
        
        # Return minimum spanning tree and sum of minimum edge weights
        return mst, mstTot

#
#   Main
#
# Instantiate MST graph
g = kMSTGraph()

# Read jobs from file
with open('clustering1.txt', 'r') as f:
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
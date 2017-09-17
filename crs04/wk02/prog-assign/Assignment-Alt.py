#   Stanford Algorithms Specialization on Coursera
#   Course 04
#   Week 02 - Programming Assignment
#
#   2017-09-17
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from datetime import datetime
from itertools import combinations

class tspGraph:
    """Basic graph class with traveling salesman methods.
    
    """

    DefaultWeight = 1
    """int: Default edge weight when not specified."""
    
    Inf = float('inf')
    """float: Shorthand for infinity."""
    
    MaxNodeCount = 31
    """int: Maximum number of supported nodes."""
    
    def __init__(self, nodes = None):
        """Initalize a new graph with optional list of edges.
        
        Args:
            nodes(:obj:`list` of :obj:`list`, optional): List of nodes with
                format (name, x, y).
        """
        self.__nodes = []
        self.__nodesRev = {}
        self.__nodeDist = [[]]
        if nodes is not None: self.addNodeList(nodes)

    @property
    def nodeCount(self):
        """int: Number of nodes"""
        return len(self.__nodes)
    
    def addNode(self, name, x, y):
        """Add a single node to the graph.
        
        Args:
            name (:hashable:): Node name.
            x (float): X position of new node.
            y (float): Y position of new node.
                property DefaultWeight.
        """
        i = self.nodeCount
        self.__nodes.append((float(x), float(y)))
        self.__nodesRev[name] = i

    def addNodeList(self, nodes):
        """Add multiple nodes from a list.
        
        Args:
            nodes(:obj:`list` of :obj:`list`): List of nodes with format
                (name, x, y).
        """
        for n in nodes:
            self.addNode(n[0], n[1], n[2])
            
    def calcNodeDists(self):
        self.__nodeDist = [[0 for x in range(self.nodeCount)]\
            for y in range(self.nodeCount)\
        ] 
        for i in xrange(0, self.nodeCount):
            for j in xrange(0, self.nodeCount):
                self.__nodeDist[i][j] = 0 if i == j else (
                    (self.__nodes[i][0] - self.__nodes[j][0])**2 + \
                    (self.__nodes[i][1] - self.__nodes[j][1])**2
                )**(0.5)
            
    def minTSP(self):
        """Return the shortest path length for traveling salesman.
        
        Returns:
            float: Length of the minimum path visiting every node exactly once.
        """
        # Raise error if graph has too many nodes
        if self.nodeCount > self.MaxNodeCount:
            raise NotImplementedError("The graph is too large with %d nodes. \
                Please restrict to graphs with %d or fewer nodes." %\
                (self.nodeCount, self.MaxNodeCount)\
            )
        
        # Calculate all node distances
        self.calcNodeDists()

        # Initialize working dictionary
        ret = defaultdict(lambda: [self.Inf] * self.nodeCount)

        # Add single edge paths
        for i in xrange(1, self.nodeCount):
            ret[1 + i**2][i] = self.__nodeDist[0][i]
        
        # Iterate through maximum number of edges in valid paths
        for i in xrange(2, self.nodeCount):
            # Print iteration
            print "Iteration", i, "started at time", datetime.now().time()

            # Generate sets (excluding zero)
            sets = combinations(range(1, self.nodeCount), i)
            
            # Iterate through each set
            for s in sets:
                # Calculate the set mask
                sMask = 1 + sum(map(lambda i: 2**i , s))
                
                # Iterate through each node in the set
                for j in s:
                    # Calcualte the set mask without this node
                    sMask_j = sMask - 2**j
                    
                    # Iterate through the other nodes
                    for k in s:
                        if k == j: continue
                        
                        # Calcuate new, full path length
                        ln = ret[sMask_j][k] + self.__nodeDist[k][j]
                        
                        # Set path length to minimum
                        ret[sMask][j] = min(ln, ret[sMask][j])
            
        # Calculate minimum return path
        fullMask = 2**self.nodeCount - 1
        for k in xrange(1, self.nodeCount):
            # Calcuate new, full path length
            ln = ret[fullMask][k] + self.__nodeDist[k][0]
            
            # Set path length to minimum
            ret[fullMask][0] = min(ln, ret[fullMask][0])
        
        # Return shortest path length
        return ret[fullMask][0]

#
# Main
#
# Instantiate graph
g = tspGraph()

# Read nodes from file with euclidian x and y-coordinates
with open('tsp.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add node from each line
    for (i, l) in enumerate(f):
        n = map(lambda v: float(v), l.strip().split(" "))
        g.addNode(i+1, n[0], n[1])

# Print graph summary
print "Graph with %d nodes." % (g.nodeCount)

# Print shortest traveling salesman path
print "Shortest traveling salesman path has length %.2f." % (g.minTSP())
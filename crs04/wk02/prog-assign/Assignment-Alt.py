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
        self.__nodes = defaultdict(lambda: None)
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
        self.__nodes[name] = (float(x), float(y))

    def addNodeList(self, nodes):
        """Add multiple nodes from a list.
        
        Args:
            nodes(:obj:`list` of :obj:`list`): List of nodes with format
                (name, x, y).
        """
        for n in nodes:
            self.addNode(n[0], n[1], n[2])

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
        
        # Create node bitmasks and notter (for getting edges not in a set)
        masks = dict(map(lambda (i, k): (k, 2**i), \
            enumerate(self.__nodes.keys())\
        ))
        notter = 2**(self.nodeCount) - 1
        
        # Initialize working dictionaries
        curr = {1:{1:0}}
        prev = {}
        
        # Iterate through maximum number of edges in valid paths
        for i in xrange(1, self.nodeCount + 1):
            # Print iteration
            print "Iteration", i, "started at time", datetime.now().time()
            
            # Swap working dictionaries
            prev = curr
            curr = defaultdict(lambda: defaultdict(lambda: self.Inf))
            
            # Iterate through previous node sets
            for s in prev.keys():
                # Get nodes not in set; NOTE: final iteration of outer for loop
                # returns to starting node
                notS = 1 if i == self.nodeCount else s ^ notter
                
                # Iterate through last node in set
                for k in prev[s].keys():
                    # Iterate through all nodes
                    for j in self.__nodes.keys():
                        # Calcuate new, full path length
                        ln = prev[s][k] + (\
                            (self.__nodes[k][0] - self.__nodes[j][0])**2 + \
                            (self.__nodes[k][1] - self.__nodes[j][1])**2\
                        )**(0.5)
                        
                        # Add path to current node if not in set and has minimum
                        # length for current paths
                        if notS & masks[j] == masks[j] and \
                            curr[s | masks[j]][j] > ln\
                        :
                            curr[s | masks[j]][j] = ln
        
        # Return shortest path length
        return curr[notter][1]

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
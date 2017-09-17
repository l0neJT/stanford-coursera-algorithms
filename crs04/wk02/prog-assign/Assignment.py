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
    
    def __init__(self, edges = None):
        """Initalize a new graph with optional list of edges.
        
        Args:
            edges(:obj:`list` of :obj:`list`, optional): List of edges in format
                [head, tail, weight]. Weight is optional.
        """
        self.__nodes = defaultdict(lambda: {"tails":[], "heads":[]})
        self.__edges = []
        if edges is not None: self.addEdgeList(edges)

    @property
    def nodeCount(self):
        """int: Number of nodes"""
        return len(self.__nodes)
    
    @property
    def edgeCount(self):
        """int: Number of edges"""
        return len(self.__edges)
    
    def addEdge(self, tail, head, weight = None):
        """Add a single edge to the graph. Creates necessary nodes if missing.
        
        Args:
            tail (:hashable:): Tail node of the new edge.
            head (:hashable:): Head node of the new edge.
            weight (int, optional): Weight of the edge. Defaults to class
                property DefaultWeight.
        """
        weight = self.DefaultWeight if weight is None else weight
        
        # Add edge
        idx = self.edgeCount
        self.__edges.append((tail, head, weight))
        
        # Add edge reference to nodes
        self.__nodes[head]["heads"].append(idx)
        self.__nodes[tail]["tails"].append(idx)

    def addEdgeList(self, edges):
        """Add multiple edges from a list. Creates necessary nodes if missing.
        
        Args:
            edges (:obj:`list` of :obj:`list`): List of edges in format [head,
                tail, weight]. Weight is optional.
        """
        for e in edges:
            self.addEdge(e[0], e[1], e[2] if len(e) > 2 else None)

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
        curr = {1:{masks[1]:0}}
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
                    # Get all incident edges
                    edges = self.__nodes[k]["heads"]
                    edges.extend(self.__nodes[k]["tails"])
                    
                    # Iterate through all edges
                    for e in set(edges):
                        edge = self.__edges[e]
                        j = edge[1] if edge[0] == k else edge[0]
                        ln = prev[s][k] + edge[2] * 1.0
                        
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
# Create temporary arrays for nodes and edges
nodes = []
edges = []

# Read nodes from file with euclidian x and y-coordinates
with open('tsp.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add node from each line
    for l in f:
        node = map(lambda v: float(v), l.strip().split(" "))
        iNode = len(nodes)
        
        # Create edges to all preceding nodes
        for i, n in enumerate(nodes):
            edges.append([i+1, iNode+1, \
                ((n[0] - node[0])**2 + (n[1] - node[1])**2)**(0.5)\
            ])
        
        # Add node
        nodes.append(node)

# Instantiate graph
g = tspGraph(edges)

# Print graph summary
print "Graph with %d nodes and %d edges." % (g.nodeCount, g.edgeCount)

# Print shortest traveling salesman path
print "Shortest traveling salesman path has length %.2f." % (g.minTSP())
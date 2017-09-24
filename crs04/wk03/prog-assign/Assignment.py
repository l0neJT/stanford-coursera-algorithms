#   Stanford Algorithms Specialization on Coursera
#   Course 04
#   Week 03 - Programming Assignment
#
#   2017-09-23
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from scipy.spatial.distance import pdist, squareform
import time

class tspGraph:
    """Basic graph class with traveling salesman methods.
    
    """

    DefaultWeight = 1
    """int: Default edge weight when not specified."""
    
    Inf = float('inf')
    """float: Shorthand for infinity."""
    
    MaxNodeCount = 31
    """int: Maximum number of supported nodes for non-heuristic TSP methods."""
    
    def __init__(self, nodes = None):
        """Initalize a new graph with optional list of edges.
        
        Args:
            nodes(:obj:`list` of :obj:`list`, optional): List of nodes with
                format (name, x, y).
        """
        self.__nodes = []
        self.__nodeNames = []
        self.__nodesByName = {}
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
        self.__nodeNames.append(hash(name))
        self.__nodesByName[name] = i

    def addNodeList(self, nodes):
        """Add multiple nodes from a list.
        
        Args:
            nodes(:obj:`list` of :obj:`list`): List of nodes with format
                (name, x, y).
        """
        for n in nodes:
            self.addNode(n[0], n[1], n[2])

    @staticmethod
    def condensedIndex(i, j, n):
        """Returns the index of the element in a condensed distance matrix from
            its square distance matrix indices. Based on responses to
            https://stackoverflow.com/questions/13079563/how-does-condensed-distance-matrix-work-pdist
            
            Args:
                i (int): The first index from the square distance matrix.
                j (int): The second index from the square distance matrix.
                n (int): The lenght of the condensed distance matrix.
            
            Returns:
                int: The index of the element in a condensed distance matrix.
        """
        assert i != j, "No diagonal elements in condensed distance matrix."
        if i < j: i, j = j, i
        return n*j - j*(j + 1)/2 + i - 1 - j

    def hminTSP(self):
        """Return an approximate shortest path length for traveling salesman
            using greedy nearest neighbor heuristic.
        
        Returns:
            float: Length of the minimum path visiting every node exactly once.
        """
        # Calculte pairwise distances
        dists = pdist(self.__nodes)
        
        # Initialize path with zeroth node
        path = [(0, 0)]
        last = 0
        
        # Initialized search space
        search = range(1, self.nodeCount)
        
        # While path is incomplete (i.e., iterate n - 1 times)
        for n in xrange(1, self.nodeCount):
            # Capture start time for run time analysis
            start = time.time()
            
            # Initialize nearest neighbor
            nnD, nnI, schI = self.Inf, None, None
            
            # Iterate through nodes in search space
            for i, this in enumerate(search):
                # Get distance from last node
                d = dists[tspGraph.condensedIndex(last, this, self.nodeCount)]
                
                # Update nearest neighbor if this node closer
                if nnD > d or (nnD == d and this < nnI):
                    nnD, nnI, schI = d, this, i
            
            # Add nearest neighbor to path
            path.append((nnI, nnD))
            
            # Remove nearest neighbor from search space
            del search[schI]
            
            # Set neighbor as last node
            last = nnI
            
            # Print ellapsed time
            if n % 100 == 0:
                print "Iteration %d took %s seconds..." % (n, time.time() - start)
        
        # Finalize path by returning to starting node
        path[0] = (0, dists[tspGraph.condensedIndex(last, 0, self.nodeCount)])
        
        # Return path length
        return sum(map(lambda p: p[1], path))

def main():
    # Initialize graph node array
    g = tspGraph()
    
    # Read nodes from file with euclidian x and y-coordinates
    with open('nn.txt', 'r') as f:
        # Skip first line
        next(f)
        
        # Create and add node from each line
        for l in f:
            n = map(lambda v: float(v), l.strip().split(" "))
            g.addNode(n[0], n[1], n[2])
        
    # Print nodes from list for debugging
    print "Graph with %d nodes." % g.nodeCount
    
    # Calculate approximate shortest path
    pathLength = g.hminTSP()
    
    # Print approximate shortest path
    print "Approximate shortest path has length %.2f." % pathLength

if __name__ == "__main__":
    start = time.time()
    main()
    print("Total runtime: %s seconds" % (time.time() - start))
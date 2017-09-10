#   Stanford Algorithms Specialization on Coursera
#   Course 04
#   Week 01 - Programming Assignment
#
#   2017-09-09
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict

class Graph:
    """Basic graph class with minimum path methods.
    
    """

    DefaultWeight = 1
    """int: Default edge weight when not specified."""
    
    Inf = float('inf')
    """float: Shorthand for infinity."""
    
    def __init__(self, edges = None):
        """Initalize a new graph with optional list of edges.
        
        Args:
            edges(:obj:`list` of :obj:`list`, optional): List of edges in format
                [head, tail, weight]. Weight is optional.
        """
        self.__nodes = defaultdict(lambda: {"tails":[], "heads":[]})
        self.__edges = []
        if edges is not None: pass
    
    @property
    def nodeCount(self):
        """int: Count nodes"""
        return len(self.__nodes)
    
    @property
    def edgeCount(self):
        """int: Count edges"""
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
        
        # Add nodes
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
    
    def shortestPathBellmanFord(self, node, returnEdges = False):
        """Return the shortest path from a single node to all other nodes
        
        Args:
            nodes(:hashable:): Starting node.
            returnEdges(boolean, optional): Indicator to return a list of edges.
                Defaults to False (returns path length).
        
        Returns:
            :obj:`dict`: All nodes with their shortest path length from starting
                node and [optional] full paths as an ordered list of nodes.
        """
        # Initialize working dictionaries and next edges to check
        curr = dict(map(lambda k: (k, (0, k) if k == node else (self.Inf, None)),\
            self.__nodes.keys()))
        prev = {}
        edges = self.__nodes[node]["tails"]
        
        # Iterate through maximum number of edges in valid paths
        for i in xrange(1, self.nodeCount):
            # Break if no edges to check (i.e. no nodes updated in previous
            # iteraton)
            if len(edges) == 0: break
        
            # Swap working dictionaries and initialize empty list of nodes
            # updated this iteration
            prev = curr
            curr = prev.copy()
            updated = []
            
            # Iterate through edges to check
            for e in edges:
                # Get edge components
                tail, head, weight = self.__edges[e]
                
                # Update head node if new path length less than previous
                if prev[tail][0] + weight < curr[head][0]:
                    curr[head] = (prev[tail][0] + weight, tail)
                    updated.append(head)
                
            # Determine edges to check in next iteration
            edges = []
            for node in set(updated): edges.extend(self.__nodes[node]["tails"])
            
        # Return None if negative cycle found
        for e in edges:
            tail, head, weight = self.__edges[e]
            if curr[tail][0] + weight < curr[head][0]: return None
        
        # Create return dictionary
        ret = dict(map(lambda k: (k, {"length":curr[k][0]}), curr.keys()))
        
        # Reconstruct full paths if required
        if returnEdges:
            # Iterate through return dictionary
            for k in ret.keys():
                # Set path to None and continue if node has not parent
                if curr[k][1] is None:
                    ret[k]["path"] = None
                    continue
                
                # Initialize path with node at tail
                ret[k]["path"] = [k]
                
                # Insert parent at head of path until no parent found
                parent = curr[k][1]
                while parent is not None and parent != ret[k]["path"][0]:
                    ret[k]["path"].insert(0, parent)
                    parent = curr[parent][1]
        
        # Return
        return ret
        
#
# Main
#
# Instantiate graph
g = Graph()

# Read edges from file
with open('g3.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add edge from each line
    for l in f:
        e = l.strip().split(" ")
        g.addEdge(int(e[0]), int(e[1]), int(e[2]))

# Print graph summary
print "Graph with %d nodes and %d edges." % (g.nodeCount, g.edgeCount)
sp1 = g.shortestPathBellmanFord(1)
print sp1
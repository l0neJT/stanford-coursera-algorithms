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
        self.__nodes = defaultdict(lambda: {"partition":None, "rank":0})
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

    def __getRoot(self, nodeKey):
        """Return root partition for given node.
        
        Args:
            nodeKey (:obj:): Target node
        """
        parentNode = self.__nodes[nodeKey]["partition"]
        if parentNode is None: return None
        if parentNode == nodeKey: return nodeKey
        return self.__getRoot(parentNode)

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
        self.__nodes[head]
        self.__nodes[tail]
    
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
        
        # Set all node partition indices to None
        for k in self.__nodes.iterkeys():
            self.__nodes[k]["partition"] = None
            self.__nodes[k]["rank"] = 0
        
        # Iterate through edges from smallest to largest adding those that
        # do not create a cycle to the MST
        for e in self.__edges:
            tailP = self.__nodes[e[0]]["partition"]
            headP = self.__nodes[e[0]]["partition"]
            
            # if e[0] == 25 and e[1] == 48:
            #     print mst
            #     print partitions
            #     print tailPartitionIndex
            #     print headPartitionIndex
            #     break
            
            # Set tail as partition if neither tail nor head previously seen
            if tailP is None and headP is None:
                self.__nodes[e[0]]["partition"] = e[0]
                self.__nodes[e[1]]["partition"] = e[0]
                self.__nodes[e[0]]["rank"] = 1
            
            # Copy tail partition index to head if head not previously seen
            elif headP is None:
                self.__nodes[e[1]]["partition"] = self.__getRoot(tailP)
            
            # Copy head partition index to tail if tail not previously seen
            elif tailP is None:
                self.__nodes[e[0]]["partition"] = self.__getRoot(headP)
                
            # Merge partitions if head and tail not in same
            else:
                tailRoot = self.__getRoot(tailP)
                headRoot = self.__getRoot(headP)
                
                # Continue to next edge if tail and head in same partition
                if tailRoot == headRoot: continue

                tailRank = self.__nodes[tailRoot]["rank"]
                headRank = self.__nodes[headRoot]["rank"]
            
                # Merge head into tail if tail has higher rank
                if tailRank > headRank:
                    self.__nodes[headRoot]["partition"] = tailRoot
                    
                # Merge tail into head if head has higher rank
                elif tailRank < headRank:
                    self.__nodes[tailRoot]["partition"] = headRoot
                
                # Merge tail into head and increment tail rank otherwise:
                else:
                    self.__nodes[tailRoot]["partition"] = headRoot
                    self.__nodes[headRoot]["rank"] += 1
            
            # Add edge if any of the above condition is True
            mst.append(e)
            mstTot = mstTot + e[2]
                
            # # Break loop if MST complete
            # if len(mst) == self.nodeCount - 1: break
        
        # Return minimum spanning tree and sum of minimum edge weights
        return mst, mstTot

#
#   Main
#
# Instantiate MST graph
g = kMSTGraph()

# Read jobs from file
with open('clustering1-example-50-solution-142.txt', 'r') as f:
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
print mst[:49]
print mst[49:]
print len(mst), mstTot
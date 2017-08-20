#   Stanford Algorithms Specialization on Coursera
#   Course 03
#   Week 03 - Programming Assignment - Part 2: Maximum Weight Independent Set
#       of a path graph
#
#   2017-08-19
#   Logan J Travis
#   loganjtravis@gmail.com

class mwis:
    """Find maximum weight independent set of a path graph.
    
    """
    
    def __init__(self, nodes = None):
        """Initialize path graph.
        
        Args:
            :obj:`list` of int, optional: Path graph represented by an ordered
                list of node values.
        """
        self.__nodes = []
        """:obj:`list` of int, private: Path graph represented by an ordered
            list of node values.
        """
        
        # Add nodes if provided
        if nodes is not None: self.extendNodes(nodes)
    
    @property
    def nodeCount(self):
        """int: Number of nodes."""
        return len(self.__nodes)
    
    def appendNode(self, value):
        """Append a node to the path graph.
        
        Args:
            int: Node value.
        """
        if type(value) is not int:
            raise TypeError("Path graph only supports integer node values. Input\
                has type %s." % str(type(value)))
        self.__nodes.append(value)
    
    def extendNodes(self, nodes):
        """Extend the path graph with additional nodes.
        
        Args:
            :obj:`list` of int: Path graph represented by an ordered list of
                node values.
        Raises:
            TypeError: If any node value is not type `int`.
        """
        for n in nodes: self.appendNode(n)

    def getMaxWeightIndependentSet(self):
        """Return list of nodes in the maximum weight independent set for the
            path graph.
        
        Returns:
            :obj:`list` of :obj:`tuple` of int: List of tuples (node position, 
                node value).
        """
        # Initialize tentative inclusion and final results list
        incl = []
        rslt = []
        
        # Iterate through each node adding that node if its value plus the
        # cumulative value of decisions for node at index - 2 is greater than
        # the cumulative decisions for node value at index - 1.
        for i in xrange(0, self.nodeCount):
            n_2 = incl[i - 2][0] if i > 1 else 0
            n_1 = incl[i - 1][0] if i > 0 else 0
            n = self.__nodes[i]
            incl.append((n + n_2, True) if n + n_2 > n_1 else (n_1, False))
        
        # Reverse through inclusion list (right to left on the path graph) 
        # to reconstruct the set with the maximum weight.
        i = self.nodeCount - 1
        while i >= 0:
            # If node included, append position to result and move to index - 2.
            # Else, check node at index - 1.
            if incl[i][1]:
                rslt.append((i, self.__nodes[i]))
                i -= 2
            else:
                i -= 1
        
        # Return result set
        return rslt

#
#   Main
#
# Instantiate maximum weight independent set
mwis = mwis()

# Read jobs from file
with open('mwis.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add node value from each line
    for l in f:
        mwis.appendNode(int(l.strip()))

# Print graph properties
print "Path graph with %d nodes." % mwis.nodeCount
mwisNodes = mwis.getMaxWeightIndependentSet()

# Print one-indexed list of nodes in the maximum weight independent set along
# with the sum of their values.
print "Maxium weight: %d" % sum(map(lambda n: n[1], mwisNodes))
oneIndexed = map(lambda n: (n[0] + 1, n[1]), mwisNodes)
# print oneIndexed

# Print only target nodes for assignment
tgtNodes = [1, 2, 3, 4, 17, 117, 517, 997]
print "Filtered Nodes for Assignment: %s" % str(\
    filter(lambda n: n[0] in tgtNodes, oneIndexed)\
)
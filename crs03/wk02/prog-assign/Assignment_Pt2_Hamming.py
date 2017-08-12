#   Stanford Algorithms Specialization on Coursera
#   Course 03
#   Week 02 - Programming Assignment - Part 2: Hamming Distance K-Clusters
#
#   2017-08-012
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from itertools import combinations
from array import array

class HamGraph (object):
    """Graph for quickly calculating k-clusters for based on Hamming distance.
    
    """

    def __init__(self, bitLength, nodes = None):
        """Initialize graph.
        
        Args:
            bitLength (int): The number of bits used for node identifiers.
            nodes (:obj:`list` of int, optional): An initial list of node
                identifiers.
        """
        self.__bitLength = bitLength
        self.__nodes = {}
        if nodes is not None: self.addNodeList(nodes)

    @property
    def bitLength(self):
        """int: The number of bits used for node identifiers."""
        return self.__bitLength
    
    @property
    def nodeCount(self):
        """int: The number of nodes in the graph."""
        return len(self.__nodes)

    def __generateMasks(self, maxDistance):
        """Return bit masks for XOR with a node identifier to create a list of
            other nodes to search.
            
        Args:
            maxDistance (int): The maximum distance permited between nodes.
        
        Returns:
            :obj:`list` of int: The bit masks.
        """
        masks = [0]
        for d in xrange(1, maxDistance + 1):
            for c in combinations(range(self.bitLength), d):
                masks.append(reduce(lambda acc, v: acc + pow(2, v), c))
        return set(masks)

    def __getRoot(self, nodeKey):
        """Return root partition for given node.
        
        Args:
            nodeKey (:obj:): Target node
        """
        parentNode = self.__nodes[nodeKey]["partition"]
        if parentNode is None: return None
        if parentNode == nodeKey: return nodeKey
        return self.__getRoot(parentNode)

    def addNode(self, node):
        """Add a single node.
        
        Args:
            node (int): The node identifier to add.
        
        Raises:
            ValueError: If the node identifer requires more bits to represent
                than the graph bit length.
        """
        if node.bit_length() > self.bitLength:
            raise ValueError("Could not represent `node` with within the graph\
                bit length of" + self.bitLength + ".")
        self.__nodes[node] = {"partition":None, "rank":0}
    
    def addNodeList(self, nodes):
        """Add multiple nodes from a list.
        
        Args:
            nodes (:obj:`list` of int, optional): A list of node identifiers.
        ValueError: If any one node identifer requires more bits to represent
                than the graph bit length.
        """
        for n in nodes:
            self.addNode(n)

    def kClustersAtSpacing(self, spacing = 2):
        """Return clusters meeting the spacing requirement where spacing in the
            minimum edge weight between any two nodes in difference clusters.

        Args:
            spacing (int): The require spacing for clusters.

        Returns:
            :obj:`dict` of :obj:`list` of int: The clusters. 
            
        """
        clusters = defaultdict(list)
        masks = self.__generateMasks(spacing - 1)
        
        # Set all node partition indices to None
        for k in self.__nodes.iterkeys():
            self.__nodes[k]["partition"] = None
            self.__nodes[k]["rank"] = 0
        
        # Iterate through nodes finding all other nodes at a distance less
        # than spacing
        for nKey in self.__nodes.keys():
            for m in masks:
                nP = self.__nodes[nKey]["partition"]
                neighborKey = nKey ^ m
                
                # Continue if neighbor is self
                if nKey == neighborKey: continue
                
                # Get neighbor parition; continue on key error.
                try:
                    neighborP = self.__nodes[neighborKey]["parition"]
                except KeyError: continue

                # Set this node as partition if neither this node nor neighbor
                # previously seen
                if nP is None and neighborP is None:
                    self.__nodes[nKey]["partition"] = nP
                    self.__nodes[neighborKey]["parition"] = nP
                    self.__nodes[nKey]["rank"] = 1
                
                # Copy this node partition to neighbor if neighbor not
                # previously seen
                elif neighborP is None:
                    self.__nodes[neighborKey]["partition"] = self.__getRoot(nP)
                
                # Copy neighbor partition to this node if this node not
                # previously seen
                elif nP is None:
                    self.__nodes[nKey]["partition"] = self.__getRoot(neighborP)
                    
                # Merge partitions if this node and neighboer not in same
                else:
                    nRoot = self.__getRoot(nP)
                    neighborRoot = self.__getRoot(neighborP)
                    
                    # Continue to next neighbor if tail and head in same
                    # partition
                    if nRoot == neighborRoot: continue
    
                    nRank = self.__nodes[nRoot]["rank"]
                    neighborRank = self.__nodes[neighborRoot]["rank"]
                
                    # Merge neighbor into this node if this node has higher rank
                    if nRank > neighborRank:
                        self.__nodes[neighborRoot]["partition"] = nRoot
                        
                    # Merge this node into neighbor if neighbor has higher rank
                    elif nRank < neighborRank:
                        self.__nodes[nRoot]["partition"] = neighborRoot
                    
                    # Merge this node into neighbor and increment neighbor
                    # otherwise
                    else:
                        self.__nodes[nRoot]["partition"] = neighborRoot
                        self.__nodes[neighborRoot]["rank"] += 1

            # Return dictionary of clusters
            for k in self.__nodes.iterkeys():
                clusters[self.__getRoot(k)].append(k)
            return clusters

#
#   Main
#
# Instantiate Hamming cluster graph
g = HamGraph(12)

# Read jobs from file
with open('clustering2-example-200-12-solution-4.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add node from each line
    for l in f:
        bitList = map(int, l.strip().split(" "))
        val = 0
        for bit in bitList:
            val = (val << 1) | bit
        g.addNode(val)

# Print graph properties
print "Graph with", g.nodeCount, "nodes and", g.bitLength, "bit length."

# Print clusters with spacing 3
print g.kClustersAtSpacing(3)
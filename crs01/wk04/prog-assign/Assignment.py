#   Stanford Algorithms Specialization on Coursera
#   Course 01
#   Week 04 - Programming Assignment
#
#   2017-07-02
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from string import rstrip
import random

#
def contract(a, b, nodes, nodesBack):
    # Create mereged key
    key = a + '::' + b
    
    # Add merged key to nodes and back pointer dictionary
    # NOTE: Removes original nodes and self references
    nodes[key].extend(nodes.pop(a))
    nodes[key].remove(b)
    nodes[key].extend(nodes.pop(b))
    nodes[key].remove(a)

    nodesBack[key].extend(nodesBack.pop(a))
    nodesBack[key].remove(b)
    nodesBack[key].extend(nodesBack.pop(b))
    nodesBack[key].remove(a)
    
    # Update other nodes with merged key
    for n in nodesBack[key]:
        for i, v in enumerate(nodes[n]):
            if v == a or v == b:
                nodes[n][i] = key
    
    return key

#
# Main
#

# Set line delimeter
delim = '\t'

# Create nodes and back pointer dictionaries with missing constructor set to empty list
nodes = defaultdict(list)
nodesBack = defaultdict(list)

# Open file and split into lines
f = open('AdjacencyList.txt', 'r')

# Populate nodes and back pointer dictionaries
for line in list(f):
    print line
    
    # Split line on delimeter
    l = rstrip(line, delim + '\r\n').split(delim)
    
    # For each value after the first, update nodes and back pointer dictionaries
    for val in l[1:]:
        nodes[l[0]].append(val)
        nodesBack[val].append(l[0])

# print nodes
# print nodesBack


#
# for i in xrange(1, 10):
#     a = random.choice(nodes.keys())
#     b = random.choice(nodes[a])
#     print i, a, nodes[a], b, nodes[b]
#     key = contract(a, b, nodes, nodesBack)
#     print nodes[key]
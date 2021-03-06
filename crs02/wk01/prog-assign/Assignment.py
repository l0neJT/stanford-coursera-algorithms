#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 01 - Programming Assignment
#
#   2017-07-09
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from string import rstrip
import json
# import sys

#
def foundChild(edge, parent, explored):
    child = edge[1] if edge[0] == parent else edge[0]
    return None if explored[child] else child

#
def dfsIter(nodes, edges, nodeOrder = [], finishTime = None):
    # Create empty explored and SCC dictionaries
    explored = defaultdict(lambda: False)
    scc = defaultdict(list)
    
    # Populate node order from nodes if empty
    nodeOrder = list(nodes.keys()) if len(nodeOrder) == 0 else nodeOrder
    
    for leader in nodeOrder:
        
        # Continue if explored
        if explored[leader]: continue
    
        print leader

        # Else initialize stack with self and iterate until empty
        stack = [leader]
        while len(stack) > 0:
            
            # print stack
            
            # Pop last node from stack and mark explored
            n = stack.pop()
            explored[n] = True
            
            # Find first unexplored child node
            child = None
            for e in nodes[n]:
                child = foundChild(edges[e], n, explored)
                if child is not None: break
            
            # Extend stack with node and child if not None
            if child is not None: stack.extend([n, child])
            
            # Else add node to SCC then append to finishTime if not None
            else:
                scc[leader].append(n)
                if finishTime is not None: finishTime.append(n)
    
    # return SCC
    return scc

#
def dfs(nodes, n, edges, explored, finishTime = None, leaderNodes = None, leader = None):
    
    # Mark node explored
    explored[n] = True
    
    # Add leader node if not None
    if leaderNodes is not None: leaderNodes[leader].append(n)
    
    # Construct list of child nodes
    children = list(map(lambda e: edges[e][1] if edges[e][0] == n else edges[e][0], nodes[n]))
    # print n, children
    for child in children:
        
        # Continue if explored
        if explored[child]: continue
    
        # Else recursively run depth-first search
        dfs(nodes, child, edges, explored, finishTime, leaderNodes, leader)
    
    # Append node to finish time if not None
    if finishTime is not None: finishTime.append(n)

#
# Main
#

# Set recursion limit; REMOVED after still failed
# sys.setrecursionlimit(100000)

# Set line delimeter
delim = ' '

# Create nodes and back pointer dictionaries with missing constructor set to empty list
nodeCount = 875714
nodes = defaultdict(list)
for i in xrange(nodeCount): nodes[i] = []
nodesBak = defaultdict(list)
for i in xrange(nodeCount): nodesBak[i] = []
edges = []

# Open file and split into lines
f = open('SCC.txt', 'r')

# Populate nodes and back pointer dictionaries
for line in list(f):
    
    # Get edge by splitting line on delimeter
    eStr = rstrip(line, delim + '\r\n').split(delim)
    
    # Convert node labels in edge from string to integer
    e = list(map(lambda str: int(str), eStr))
    # print e
    
    # Add edge and edge references to nodes
    i = len(edges)
    nodes[e[0]].append(i)
    nodesBak[e[1]].append(i)
    edges.append(e)

print 'Count nodes:', len(nodes)
print 'Count nodes in back pointer dict:', len(nodesBak)
print 'Count edges:', len(edges)

#
# Reverse DFS to get finish times
#
# Create empty finish time list and call iterative DFS on reverse node list
finishTime = []
dfsIter(nodesBak, edges, range(len(nodes), 0, -1), finishTime)

print 'Finish time list length:', len(finishTime)

#
# Normal DFS to get strongly connected components
#
scc = dfsIter(nodes, edges, list(reversed(finishTime)))
json.dump(scc, open('SCC.json', 'w'))

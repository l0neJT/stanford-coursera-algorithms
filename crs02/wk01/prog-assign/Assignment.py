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
# Set line delimeter
delim = ' '

# Create nodes and back pointer dictionaries with missing constructor set to empty list
nodes = defaultdict(list)
nodesBak = defaultdict(list)
edges = []
edgesBak = []

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

# print nodes
# print nodesBak
print edges[:10]

#
# Reverse DFS to get finish times
#
# Create empty explored dictionary and finish time list
explored = defaultdict(lambda: False)
finishTime = []

for n in xrange(len(nodes), 0, -1):
    
    # Continue to next unexplored node
    if explored[n]: continue

    # Run depth-first search updating explored and finish time
    dfs(nodesBak, n, edges, explored, finishTime)

print finishTime[:10]

#
# Normal DFS to get strongly connected components
#
# Create empty explored and leader dictionaries
explored = defaultdict(lambda: False)
leaderNodes = defaultdict(list)

for n in reversed(finishTime):
    
    # Continue to next unexplored node
    if explored[n]: continue

    # Run depth-first search updating explored and finish time
    dfs(nodes, n, edges, explored, None, leaderNodes, n)

json.dump(leaderNodes, open('leaderNodes.json', 'w'))
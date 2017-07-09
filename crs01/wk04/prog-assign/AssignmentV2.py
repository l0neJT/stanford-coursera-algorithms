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
from copy import deepcopy
from datetime import datetime
import random

# 
def updateEdge(edge, edges, thisNode, otherNode, mergeNode, nodes):
    for i, v in enumerate(edges[edge]):
        if v == a or v == b:
            edges[edge][i] = mergeNode

#
def contract(edge, edges, nodes):
    # Create mereged key
    a, b = edges[edge][0], edges[edge][1]
    key = a + '::' + b
    updatedEdges = []
    
    # Update keys for edges adjacent to node a
    for e in nodes[a]:
        for i, v in enumerate(edges[e]):
            if v == a or v == b:
                edges[e][i] = key
                updatedEdges.append(e)
    
    # Update keys for edges adjacent to node b
    for e in nodes[b]:
        for i, v in enumerate(edges[e]):
            if v == a or v == b:
                edges[e][i] = key
                updatedEdges.append(e)
    
    # Remove newly created self references
    for e in set(updatedEdges):
        if edges[e][0] == edges[e][1]:
            edges.pop(e)
            if e in nodes[a]: nodes[a].remove(e)
            if e in nodes[b]: nodes[b].remove(e)
        
    # Create and populate merged node
    nodes[key].extend(nodes.pop(a, None))
    nodes[key].extend(nodes.pop(b, None))

#
def minCut(edges, nodes):
    for i in xrange(1, len(nodes) - 1):
        edge = random.choice(edges.keys())
        contract(edge, edges, nodes)
    # print nodes
    return len(edges)

#
# Main
#
# Set line delimeter
delim = '\t'

# Create nodes and back pointer dictionaries with missing constructor set to empty list
nodes = defaultdict(list)
edges = {}

# Open file and split into lines
f = open('AdjacencyList.txt', 'r')

# Populate nodes and back pointer dictionaries
for line in list(f):

    # Split line on delimeter
    l = rstrip(line, delim + '\r\n').split(delim)
    
    # For each value after the first, update nodes and back pointer dictionaries
    a = l[0]
    for b in l[1:]:
        
        # Skip if edge already created for adjacency with b
        skip = False
        for e in nodes[b]:
            if skip: continue
            skip = True if edges[e][0] == a or edges[e][1] == a else False
        if skip: continue
        
        # Otherwise create new edge
        i = len(edges)
        nodes[a].append(i)
        nodes[b].append(i)
        edges[i] = [a, b]

minEdges = len(edges)
numTrails = pow(len(nodes), 2)
print '---INIT---'
print 'Node count:', len(nodes)
print 'Edge count:', minEdges
print 'Number of trails:', numTrails
minForOneNode = minEdges
for n in nodes.keys():
    minForOneNode = len(nodes[n]) if minForOneNode > len(nodes[n]) else minForOneNode
print 'Minimum edges for one node: ', minForOneNode

percent = numTrails // 100
start = datetime.now()
for i in xrange(1, numTrails):
    newMin = minCut(deepcopy(edges), deepcopy(nodes))
    minEdges = min(minEdges, newMin)
    if i % percent == 0:
        print i // percent , '% complete after ', (datetime.now() - start).seconds, ' seconds...'
        print 'Current minimum cut:', minEdges

# print 'Minimum cut:', minEdges
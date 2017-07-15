#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 01 - Programming Assignment - Experiments
#
#   2017-07-15
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict

class Node():
    """Document Node Class"""
    
    def __init__(self, value):
        """Document Node Class initializer"""
        self._key = hash(value)
        self._value = value
        self._tailEdges = list()
        self._headEdges = list()
    
    def __hash__(self):
        """Document Node Class hash method"""
        return self._key
    
    def __eq__(self, other):
        """Document Node class equality method"""
        return self._key == other._key
    
    def __ne__(self, other):
        """Document Node class inequality method"""
        return not(self._key == other._key)
    
    def __repr__(self):
        """Document Node class representation method"""
        return self._value
    
    def addEdgeWhereHead(self, key):
        """Document Node Class addEdgeWhereHead"""
        self._headEdges.append(key)
    
    def addEdgeWhereTail(self, key):
        """Document Node Class addEdgeWhereTail"""
        self._tailEdges.append(key)

class defaultdictKeyToConstructor(defaultdict):
    """Document defaultdictNode Class"""
    
    def __missing__(self, key):
        """Document defaultdictNode missing method
        
           Borrowed from stackoverflow post https://stackoverflow.com/a/2912455"""
        
        if self.default_factory is None:
            raise KeyError(key)
        else:
            self[key] = self.default_factory(key)
            return self[key]

class Graph():
    """Document Graph Class"""
    
    # Default edge weight when not specified
    DefaultWeight = 1
    
    def __init__(self, directed = False, edges = None):
        """Document Graph Class initializer"""
        self._nodes = defaultdictKeyToConstructor(Node)
        self._directed = directed
        self._edges = []
        
        # Add edges if not none
        if edges is not None: self.addEdgesFromIterable(edges)
    
    def addEdge(self, tail, head, weight = None):
        """Document Graph Class addEdge"""
        
        # Set edge weight to default if None
        weight = self.DefaultWeight if weight is None else weight
        
        # Get new edge position and add to edges
        i = self.getEdgeCount()
        self._edges.append([tail, head, weight])
        
        # Update node edge pointers (directed)
        self._nodes[head].addEdgeWhereHead(i)
        self._nodes[tail].addEdgeWhereTail(i)

        # Update node edge pointers (undirected)
        if not(self._directed):
            self._nodes[head].addEdgeWhereTail(i)
            self._nodes[tail].addEdgeWhereHead(i)
    
    def addEdgesFromIterable(self, edges):
        """Document Graph Class addEdgesFromList"""
        
        # Iterate through edges adding each to graph
        for edge in edges:
            self.addEdge(edge[0], edge[1], edge[2] if len(edge) > 2 else None)
    
    def getEdgeCount(self):
        """Document Graph Class getEdgeCount method"""
        return len(self._edges)
            
g = Graph(directed = True)
g.addEdgesFromIterable([['a', 'b', 1], ['b', 'c']])
print g._edges
print g._nodes
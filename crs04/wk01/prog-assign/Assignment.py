#   Stanford Algorithms Specialization on Coursera
#   Course 04
#   Week 01 - Programming Assignment
#
#   2017-09-09
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from heapq import heappush, heapify

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
    
    @staticmethod
    def __reconstructPath(nodes, returnEdges):
        """Reconstruct paths for shortest path algorithm results."""
        # Create return dictionary
        ret = dict(map(lambda k: (k, {"length":nodes[k][0]}), nodes.keys()))
        
        # Reconstruct full paths if required
        if returnEdges:
            # Iterate through return dictionary
            for k in ret.keys():
                # Set path to None and continue if node has not parent
                if nodes[k][1] is None:
                    ret[k]["path"] = None
                    continue
                
                # Initialize path with node at tail
                ret[k]["path"] = [k]
                
                # Insert parent at head of path until no parent found
                parent = nodes[k][1]
                while parent is not None and parent != ret[k]["path"][0]:
                    ret[k]["path"].insert(0, parent)
                    parent = nodes[parent][1]
        
        # Return
        return ret
    
    def spBellmanFord(self, node, returnEdges = False):
        """Return the shortest path from a single node to all other nodes using
            then Bellman-Ford algorithm.
        
        Args:
            node(:hashable:): Starting node.
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
        
        # Return shortest paths
        return Graph.__reconstructPath(curr, returnEdges)
    
    @staticmethod
    def __swapHeapNodes(heap, nodes, i, j):
        """Swap heap nodes."""
        iNode, jNode = heap[i][1], heap[j][1]
        heap[i], heap[j] = heap[j], heap[i]
        nodes[iNode], nodes[jNode] = j, i
    
    @staticmethod
    def __siftup(heap, nodes, pos, stopPos):
        """Sifts node up heap from starting position up to stopping position.
            Helper for Dijkstra shortest path algorithm.
        
        """
        # Loop until past stopping position
        while pos > stopPos:
            # Set parent position
            parentPos = (pos - 1) >> 1

            # Swap if child less than parent
            if heap[pos][0] < heap[parentPos][0]:
                Graph.__swapHeapNodes(heap, nodes, pos, parentPos)
                pos = parentPos
            
            # End sift if child's first tuple is greater than or equal to parent
            else: break
    
    @staticmethod
    def __siftdown(heap, nodes, pos, stopPos = None):
        """Sifts down heap from starting position down to stopping position.
            Helper for Dijkstra shortest path algorithm.
        
        """
        # Default stopping position to end of heap
        stopPos = stopPos if not None else len(heap) - 1
        
        # Loop until past stopping position
        while pos < stopPos:
            # Set right and left child positions
            rChildPos = (pos + 1) << 1
            lChildPos = rChildPos - 1
            
            # Break if children passt stopping position
            if(lChildPos > stopPos): break
        
            # Check left child only if right past stopping position
            if(rChildPos > stopPos):
                # Swap if left child less than parent
                if heap[pos][0] > heap[lChildPos][0]:
                    Graph.__swapHeapNodes(heap, nodes, pos, lChildPos)
                    pos = lChildPos
                
                # End sift if left child greater than or equal to parent
                else: break
        
            # Determine minimum of parent, left child, and right child otherwise
            else:
                # Use heap (why not?) to order parent, left child, and right
                # child then extract position
                minHeap = [
                        (heap[pos][0], pos),
                        (heap[lChildPos][0], lChildPos),
                        (heap[rChildPos][0], rChildPos)
                    ]
                heapify(minHeap)
                
                # End sift if parent has minimum value
                if minHeap[0][1] == pos: break
            
                # Swap otherwise
                Graph.__swapHeapNodes(heap, nodes, pos, minHeap[0][1])
                pos = minHeap[0][1]
    
    @staticmethod
    def __heappush(heap, nodes, node):
        """Push a node onto the heap."""
        pos = len(heap)
        heap.append(node)
        nodes[node[1]] = pos
        Graph.__siftup(heap, nodes, pos)
    
    @staticmethod
    def __heappop(heap, nodes, pos, stopPos = None):
        """Pop a node from the heap."""
        # Default stopping position to end of heap
        stopPos = stopPos if not None else len(heap) - 1
        
        # Swap target node with stopping position, re-order heap to stopping
        # position minus one, then pop the target node
        Graph.__swapHeapNodes(heap, nodes, pos, stopPos)
        Graph.__siftdown(heap, nodes, pos, stopPos - 1)
        node = heap.pop(stopPos)
    
        # Delete node from dictionary and return
        del nodes[node[1]]
        return node

    def spDijkstra(self, node, returnEdges = False):
        """Return the shortest path from a single node to all other nodes using
            Dijkstra's algorithm.
        
        Args:
            node(:hashable:): Starting node.
            returnEdges(boolean, optional): Indicator to return a list of edges.
                Defaults to False (returns path length).
        
        Returns:
            :obj:`dict`: All nodes with their shortest path length from starting
                node and [optional] full paths as an ordered list of nodes.
        """
        # Initialize heap, not found nodes, and found nodes
        heap = map(lambda k: (\
            0 if k == node else self.Inf,\
            k,\
            k if k == node else None), self.__nodes.keys())
        nodes = dict(map(lambda (i, n): (n[1], i), enumerate(heap)))
        found = defaultdict(lambda: None)
        
        # Swap target node to beginning of heap
        Graph.__swapHeapNodes(heap, nodes, 0, nodes[node])
        
        # Iterate through nodes
        for stopPos in xrange(len(heap) - 1, -1 , -1):
            # Pop minimum node
            n = Graph.__heappop(heap, nodes, 0, stopPos)
            
            # Add to found nodes
            found[n[1]] = (n[0], n[2])
        
            # Update path length for nodes reachable from minimum node
            for e in self.__nodes[n[1]]['tails']:
                # Get edge components
                tail, head, weight = self.__edges[e]
                
                # Continue if head node already found
                if found[head] is not None: continue
            
                # Calculate new path length and update if less than current
                newLen = n[0] + weight
                if newLen < heap[nodes[head]][0]:
                    heap[nodes[head]] = (newLen, head, tail)
                    Graph.__siftup(heap, nodes, nodes[head], 0)
        
        # Return shortest paths
        return Graph.__reconstructPath(found, returnEdges)   
        
#
# Main
#
# Instantiate graph
g = Graph()

# Read edges from file
with open('g_test_dijkstra.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add edge from each line
    for l in f:
        e = l.strip().split(" ")
        g.addEdge(int(e[0]), int(e[1]), int(e[2]))

# Print graph summary
print "Graph with %d nodes and %d edges." % (g.nodeCount, g.edgeCount)
i = 4
print g.spDijkstra(i, True)
print g.spBellmanFord(i, True)
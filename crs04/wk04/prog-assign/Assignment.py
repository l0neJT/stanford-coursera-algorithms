#   Stanford Algorithms Specialization on Coursera
#   Course 04
#   Week 04 - Programming Assignment
#
#   2017-09-30
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
import time

class twoSAT:
    """Represent a 2-satisfiability ("2-SAT") statement as an implication graph
        and solve.
    
    """
    
    def __init__(self, clauses = None):
        """Initalize new implication graph representing a 2-SAT statement.
        
        Args:
            clauses(:obj:`list` of :obj:`list`, optional): List of 2-SAT clauses
                in format (a, b) where a and b are integer identifiers of two
                boolean variables. Negative integers negate the boolean variable
                represented by the same positive integer.
        """
        self.__nodes = defaultdict(lambda: {"tails":[], "heads":[]})
        self.__edges = []
    
    @property
    def nodeCount(self):
        """int: Number of nodes in the implicaton graph"""
        return len(self.__nodes)
    
    @property
    def edgeCount(self):
        """int: Number of edges in the implication graph"""
        return len(self.__edges)
    
    @property
    def clauseCount(self):
        """int: Number of clause in the 2-SAT statement"""
        return self.edgeCount / 2
    
    @property
    def variableCount(self):
        """int: Number of boolean variables in the 2-SAT statement"""
        return len(set(map(lambda k: abs(k), self.__nodes.keys())))
    
    def __addEdge(self, tail, head):
        """Add a single edge to the implication graph.
        
        Args:
            tail(int): Integer identifier for the tail node of the edge.
            head(int): Integer identifier for the head node of the edge.
        Raises:
            TypeError: If `tail` or `head` not type `int`.
        """
        # Raise error if tail or head not integer
        if type(tail) is not int or type(head) is not int: raise TypeError(\
            "`tail` and `head` must have type `int`. Have types `%s` and `%s`."\
            % (str(type(tail)), str(type(head)))\
        )
        edgePos = self.edgeCount
        self.__edges.append([tail, head])
        self.__nodes[tail]["tails"].append(edgePos)
        self.__nodes[head]["heads"].append(edgePos)
    
    def addClause(self, a, b):
        """Add a single clause to the 2-SAT statement.
        
        Args:
            a(int): Integer representation of the first boolean variable. A
                Negative integer negates the boolean variable represented by the
                same positive integer.
            b(int): Integer representation of the second boolean variable. A
                Negative integer negates the boolean variable represented by the
                same positive integer.
        """
        self.__addEdge(-1 * a, b)
        self.__addEdge(-1 * b, a)
    
    def dfs(self, node, visited = None, reverse = False):
        """Perform depth first search on the implication graph.
        
        Args:
            node(int): Integer identifier for current node.
            visited(:obj:`dict`, optional): Dictionary of visited nodes.
                Defaults to empty.
            reverse(bool, optional): Indicator to reverse all edge directions.
                Defaults to False.
        Returns:
            :obj:`list` of int: Found nodes as a stack in DFS order (i.e., 
                leaves first).
        """
        # Initialize return stack
        found = []

        # Mark current node as visited
        visited = dict(map(lambda k: (k, False), self.__nodes.keys()))\
            if visited is None else visited
        visited[node] = True
        
        # Get edges to search
        edges = self.__nodes[node]["heads"] if\
            reverse else\
            self.__nodes[node]["tails"]
        
        # Iterate through edges
        for e in edges:
            # Determine child node
            n = self.__edges[e][0] if\
                self.__edges[e][1] == node else\
                self.__edges[e][1]
            
            # Continue if child node visited
            if visited[n]: continue
        
            # Extend stack with recursive DFS result
            found.extend(self.dfs(n, visited, reverse))
        
        # Append this node to stack and return
        found.append(node)
        return found
    
    def scc(self):
        """Determine strongly connected components using Kosaraju's algorithm.
        
        Returns:
            :obj:`list` of :obj:`list`: List of strongly connected components.
        """
        # Initialize node stack and visited dictionary
        forward = []
        visited = dict.fromkeys(self.__nodes.iterkeys(), False)
        
        # Iterate through nodes
        for n in self.__nodes.keys():
            # Continue if node visited
            if visited[n]: continue
        
            # Perform DFS and extend node stack with result
            forward.extend(self.dfs(n, visited))
        
        # Initialize return list and reset visited to False
        reverse = []
        visited = dict.fromkeys(visited.iterkeys(), False)
        
        # Iterate through node stack
        for n in forward:
            # Continue if node visited
            if visited[n]: continue
        
            # Perform reverse DFS to get strongly connected components
            reverse.append(self.dfs(n, visited, False))
        
        # Return strongly connected components
        return reverse
    
    def satisfiable(self):
        """Determine if the statement is satisfiable.
        
        Returns:
            bool: True if the statement is satisfiable, otherwise False.
        """
        # Get strongly connected components
        comp = self.scc()
        
        # Iterate through strongly connected components
        for c in comp:
            # Initialize visited dictionary
            visited = defaultdict(lambda: False)
            
            # Iterate through nodes
            for n in c:
                # Return false if the negatation of current node is in this SCC
                if visited[-1 * n]: return False
                
                # Mark current node as visited
                visited[n] = True
        
        # Return true if no SCC included a negated node pair
        return True

def main():
    # Initialize 2-SAT statement
    g = twoSAT()
    
    # Read clauses from file
    with open("2sat4.txt", "r") as f:
        # Skip first line
        next(f)
        
        # Create and add clause from each line
        for l in f:
            n = map(lambda v: int(v), l.strip().split(" "))
            g.addClause(n[0], n[1])
        
    # Print 2-SAT summary
    print "2-SAT statement with %d variables and %d clauses." %\
        (g.variableCount, g.clauseCount)
    print "Stored as an implication graph with %d nodes and %d edges." %\
        (g.nodeCount, g.edgeCount)
        
    # DEBUG Print strongly connected components
    # print g.scc()
    
    # Print whether the statement is satisfiable
    print "Statement is satisfiable: %s" % str(g.satisfiable())

if __name__ == "__main__":
    start = time.time()
    main()
    print("Total runtime: %s seconds" % (time.time() - start))
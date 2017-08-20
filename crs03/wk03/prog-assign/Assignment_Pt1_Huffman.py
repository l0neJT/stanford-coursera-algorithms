#   Stanford Algorithms Specialization on Coursera
#   Course 03
#   Week 03 - Programming Assignment - Part 1: Huffman Coding
#
#   2017-08-19
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from heapq import heapify, heappop, heappush

class huffCode:
    """Create Huffman coding from a list of symbols.
    
    """
    
    def __init__(self, symbols = None):
        """Initialize encoder.
        
        Args:
            symbols(`obj`list of `obj`list of [`obj`, int], optional): List of
                objects to encode each with an integer for determining relative
                occurrence.
        """
        self.__symbols = {}
        """:obj:`dict`, private: Dictionary of symbols (keys) and occurences
            (values).
        """
        
        self.__encodingTree = []
        """:obj:`list`, private: List of tuples used for encoding/decoding. Each
            tuple has four items with occurences as 0, object at 1, left child
            position at 2, and right child position at 3. All but occurences may
            include None.
        """
            
        self.__encoded = False
        """bool, private: Indicator whether all symbols encoded. See isEncoded
            for public property.
        """
        
        # Add symbols if provided
        if symbols is not None: self.addSymbols(symbols)

    @property
    def symbolCount(self):
        """int: Number of symbols.
        
        """
        return len(self.__symbols)
    
    @property
    def isEncoded(self):
        """bool: Indicator whether all symbols encoded.
        
        """
        return self.__encoded
    
    def addSymbol(self, symbol, occurs):
        """Add a single symbol.
        
        Args:
            symbol(`obj`): Any object. Duplicate objects ignored.
            occurs(int): An integer for determining releative occurrence.
        """
        if symbol not in self.__symbols:
            self.__symbols[symbol] = occurs
            self.__encoded = False
    
    def addSymbols(self, symbols):
        """Add multiple symbols from a list.
        
        Args:
            symbols(`obj`list of `obj`list of [`obj`, int], optional): List of
                objects to encode each with an integer for determining
                relative occurrence.
        """
        for s in symbols: self.addSymbol(s[0], s[1])
    
    def __encode(self, node, code = ""):
        """Return encoding for all symbols by recursing through encoding tree.
        
        Args:
            node(tuple): Current node in the encoding tree.
            code(str, optional): Code for current node. Defaults to empty string.
        """
        encoded = {} if node[1] is None else {node[1]:code}
        if node[2] is not None:
            encoded.update(self.__encode(self.__encodingTree[node[2]], code + "0"))
        if node[3] is not None:
            encoded.update(self.__encode(self.__encodingTree[node[3]], code + "1"))
        return encoded

    def encodeHuffman(self):
        """Return the Huffman encoding for all symbols.
        
        Returns:
            `obj`dict: Dictionary of symbols (keys) and encoded values.
        """
        # Encode symbols if not previously encoded
        if not(self.isEncoded):
            # Initialize empty symbol tree
            self.__encodingTree = []
            
            # Initialize heap with items (occurences, object, left child
            # position, right child position). Positions for use in encoding
            # tree. Since all objects occur as leaves, positions set to None.
            heap = map(\
                lambda k: (self.__symbols[k], k, None, None),\
                self.__symbols.keys()\
            )
            heapify(heap)
            
            # Iterate until all symbols merged
            while len(heap) > 1:
                # Get lowest occuring pair
                left = heappop(heap)
                rght = heappop(heap)

                # Add to encoding tree
                i = len(self.__encodingTree)
                self.__encodingTree.append(left)
                self.__encodingTree.append(rght)
                
                # Create merged symbol and push into heap
                heappush(heap, (rght[0] + left[0], None, i, i + 1))
            
            # Add root node and set self as encoded
            self.__encodingTree.append(heap[0])
            self.__encoded = True
        
        # Return encoded symbols
        return self.__encode(self.__encodingTree[-1])

#
#   Main
#
# Instantiate Huffman encoding
h = huffCode()

# Read jobs from file
with open('huffman.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add edge from each line
    i = 0
    for l in f:
        h.addSymbol(i, int(l.strip()))
        i += 1

# Print graph properties
print h.symbolCount, "symbols"
encoded = h.encodeHuffman()
# print encoded
print "Minimum bits:", min(map(lambda k: len(encoded[k]), encoded.keys()))
print "Maximum bits:", max(map(lambda k: len(encoded[k]), encoded.keys()))
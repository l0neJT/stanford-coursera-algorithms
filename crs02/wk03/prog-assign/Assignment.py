#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 03 - Programming Assignment
#
#   2017-07-22
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from collections import defaultdict
from string import rstrip
from heapq import heappush, heappop

class MMedian:
    """Maintain median value as elements added/extracted.
    
    """
    
    TieBreakers = {
        'min': lambda valMin, valMax: valMin,
        'max': lambda valMin, valMax: valMax,
        'avg': lambda valMin, valMax: (float(valMin) + float(valMax)) / float(2)
    }
    
    def __init__(self, tieBreak = 'min', startList = None):
        """Initialize lower and upper half heaps.
        
        May include optional input list read into heaps from head to tail.
        """
        
        # Initialize lower and upper half heaps
        self.lower = []
        self.upper = []
        
        # Set tie breaker to minimum if not an acceptable value
        self.tieBreak = 'min' if tieBreak not in self.TieBreakers else tieBreak
        
        # Insert values fron input list if not None
        if startList is not None:
            for i in xrange(0, len(startList)):
                # STUB
                break
    
    def getMedian(self):
        """Return median value"""
        
        # Get heap lengths
        lenLower = len(self.lower)
        lenUpper = len(self.upper)
        
        # If both empty, return None
        if lenLower == 0 and lenUpper == 0: return None
        
        # If lower heap is one longer than upper heap, return root from lower
        if lenLower - 1 == lenUpper: return -1 * self.lower[0]
        
        # If upper heap is one longer than lower heap, return root from upper
        if lenLower + 1 == lenUpper: return self.upper[0]
        
        # If heaps have equal, non-zero lengths, return based on tie breaker
        if lenLower == lenUpper:
            return self.TieBreakers[self.tieBreak](-1 * self.lower[0], self.upper[0])
        
        # Throw error if no condition above met
        raise AttributeError('Lower and upper heaps have invalid lengths.')
    
    def insert(self, value):
        """Insert new value and return resulting median"""
        
        #
        # Valid type checks
        #
        # Raise type error if type is long
        if type(value) == long:
            raise TypeError('MMedian does not support long data type at this time.')
        
        # Raise type error if type is non-numeric
        if type(value) != int and type(value) != float:
            raise TypeError('MMedian supports only integers and floats.')
        
        # Push new value into lower heap
        heappush(self.lower, -1 * value)
        
        # If lower heap length more than 1 + upper heap length, re-balance
        if len(self.lower) > len(self.upper) + 1:
            maxLower = -1 * heappop(self.lower)
            heappush(self.upper, maxLower)
        
        # Return resulting median
        return self.getMedian()

#
#   Main
#
# Instantiate median maintenance 
mm = MMedian()

# Open file, set delimeters, and set directed-ness
f = open('Median_TEST.txt', 'r')

# For each line in file, insert into median maintenance
for l in list(f):
    print mm.insert(int(l.strip()))
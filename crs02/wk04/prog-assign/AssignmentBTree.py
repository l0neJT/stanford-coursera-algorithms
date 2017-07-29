#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 04 - Programming Assignment - Binary Tree implementation
#
#   2017-07-29
#   Logan J Travis
#   loganjtravis@gmail.com

# Import progress bar
from sortedcontainers import SortedSet
from print_progress import print_progress

class TwoSum:
    """Stores a set of integers and returns the pairs of values that sum to a 
    specified total.
    
    """
    
    def __init__(self, startList = None):
        """Initialize set of integers.
        
        """
        self._intSet = SortedSet()
        if startList is not None: self.addIntegerList(startList)
    
    def addIntegerList(self, intList):
        """Add integers from list to set
        
        """
        for i in intList: self.addInteger(i)
            
    def addInteger(self, integer):
        """Add a single integer to set
        
        """
        self._intSet.add(integer)
        
    def findSums(self, totalLow, totalHigh, requireUnique = False):
        """Return set of totals in range for which at least one pair of
        integers in set existins such that x + y = total.
        
        Optional parameter for uniqueness will exclude x + x = integer.
        """
        # Flip total high and low if passed out of order
        if totalLow > totalHigh:
            swap = totalLow
            totalLow = totalHigh
            totalHigh = swap
        
        # Initalize empty found totals set
        foundTotals = set()
        
        # Iterate over each integer in the set
        for x in self._intSet:
            # Determine search range for y
            # NOTE: start index is inclusive where stop index is exclusive
            # to match behavior of SortedSet.islice()
            iStart = self._intSet.bisect_left(totalLow - x)
            iStop = self._intSet.bisect_right(totalHigh - x)
            
            # Continue if search range invalid
            if iStart >= iStop: continue
        
            # Add each sum x + y to found totals
            for y in self._intSet.islice(iStart, iStop):
                foundTotals.add(x + y)
        
        # Return found totals set
        return foundTotals


    # def sumsTo(self, total, requireUnique = False):
    #     """Return true if set has at least one integer pair that sums to target.
        
    #     Optional parameter for uniqueness will exclude integer adding to itself.
    #     """

    #     # Check each integer in the set and return true if pair exists summing
    #     # to total.
    #     for x in self._intSet:
    #         diff = total - x
    #         if requireUnique and diff == x: continue
    #         try:
    #             return self._intSet[diff]
    #         except KeyError:
    #             continue
        
    #     # Return false if no pairs found
    #     return False

#
#   Main
#
# Instantiate TwoSum
twoSum = TwoSum()

# Open file
f = open('2sum.txt', 'r')

# For each line in file, insert into median maintenance and append resulting
# median to medians list
for l in list(f):
    twoSum.addInteger(int(l.strip()))

# Search for totals
totalLow = -10000
totalHigh = 10000
requireUnique = True
print "Checking totals ranging from", totalLow, "to", totalHigh, "(inclusive)"
if requireUnique: print "***Total on unique integers ONLY***"
foundTotals = twoSum.findSums(totalLow, totalHigh, requireUnique)
print len(foundTotals)
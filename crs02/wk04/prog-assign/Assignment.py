#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 04 - Programming Assignment
#
#   2017-07-29
#   Logan J Travis
#   loganjtravis@gmail.com

# Import progress bar
from print_progress import print_progress

class TwoSum:
    """Stores a set of integers and returns the pairs of values that sum to a 
    specified total.
    
    """
    
    def __init__(self, startList = None):
        """Initialize set of integers.
        
        """
        self._intSet = {}
        self.__intMax = 0
        self.__intMin = 0
        if startList is not None: self.addIntegerList(startList)
    
    def addIntegerList(self, intList):
        """Add integers from list to set
        
        """
        for i in intList: self.addInteger(i)
            
    def addInteger(self, integer):
        """Add a single integer to set
        
        """
        self._intSet[integer] = True
        self.__intMax = integer if integer > self.__intMax else self.__intMax
        self.__intMin = integer if integer < self.__intMin else self.__intMin
    
    def getMax(self):
        """Return the current maximum integer in the set.
        
        """
        return self.__intMax
        
    def getMin(self):
        """Returns the current minimum integer in the set.
        
        """
        return self.__intMin
    
    def sumsTo(self, total, requireUnique = False):
        """Return true if set has at least one integer pair that sums to target.
        
        Optional parameter for uniqueness will exclude integer adding to itself.
        """
        
        # Quick checks for total outside (2*min, 2*max)
        if total < 2 * self.__intMin: return False
        if total > 2 * self.__intMax: return False
        
        # Check each integer in the set and return true if pair exists summing
        # to total.
        for x in self._intSet:
            diff = total - x
            if requireUnique and diff == x: continue
            try:
                return self._intSet[diff]
            except KeyError:
                continue
        
        # Return false if no pairs found
        return False

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

# Create list of total and test for each
foundTotals = []
minTotal = -10000
maxTotal = 10000
requireUnique = True
print "Checking totals ranging from", minTotal, "to", maxTotal, "(inclusive)"
if requireUnique: print "***Total on unique integers ONLY***"
for t in xrange(minTotal, maxTotal + 1):
    print_progress(t - minTotal, 1 + maxTotal - minTotal)
    if twoSum.sumsTo(t, requireUnique): foundTotals.append(t)
print "\nCount totals:", len(foundTotals)
# print "Totals found:", foundTotals

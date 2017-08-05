#   Stanford Algorithms Specialization on Coursera
#   Course 03
#   Week 01 - Programming Assignment
#
#   2017-08-05
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from sortedcontainers import SortedList
from functools import total_ordering

@total_ordering
class DifferenceJob:
    """
    
    """
    def __init__(self, weight = 1, runtime = 1):
        """Instanciate a difference job with weight and runtime
        
        """
        self._weight, self._runtime = weight, runtime
        self._difference = weight - runtime
    
    def __eq__(self, other):
        """Return true if two difference jobs have equal weight and runtime
        
        """
        return self._weight == other._weight and self._runtime == other._runtime
    
    def __lt__(self, other):
        """Return true if this difference job has a lower difference than 
        another difference job. Ties broken by the lesser weight.another
        
        """
        return (
            self._difference < other._difference or (
                self._difference == other._difference
                and self._weight < other._weight
            )
        )
        
    def __str__(self):
        """Return a string representation
        
        """
        return "{\"_difference\":" + str(self._difference) + ",\"_weight\":" + str(self._weight) + ",\"_runtime\":" + str(self._runtime) + "}"
        
    def __repr__(self):
        """Return string representation
        
        """
        return str(self)
#
#   Main
#
test = SortedList()
jobs = [
    DifferenceJob(1,2),
    DifferenceJob(1,3),
    DifferenceJob(1,4),
    DifferenceJob(2,5)
]
test.update(jobs)
print test
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
    """A single job for use in a difference schedule.
    
    Intended only to achieve the outcomes required for the programming
    assignment in week one (1) of course three (3) of the Stanford Algorithms
    Specialization offered through Coursera.

    """
    def __init__(self, weight = 1, runtime = 1):
        """Instantiate a difference job with weight and runtime.Instantiate
        
        Args:
            weight (int): Value for completing the job. Defaults to one (1).
            runtime (int): Time required to complete the job once started.
                Defaults to one (1).
        """
        self.__weight, self.__runtime = weight, runtime
    
    @property
    def weight(self):
        """int: Value for completing the job."""
        return self.__weight
    
    @property
    def runtime(self):
        """int: Time required to complete the job once started."""
        return self.__runtime
    
    @property
    def difference(self):
        """int: Calculated by subtracting runtime from weight."""
        return self.weight - self.runtime
    
    def __eq__(self, other):
        """Return equality comparison between this difference job and another.
        
        Args:
            other(:obj:DifferenceJob): The comparison difference job.
        
        Returns:
            bool: True if this difference job and the other have equal weight
                and runtime properties. False otherwise.
        """
        return self.weight == other.weight and self.runtime == other.runtime
    
    def __lt__(self, other):
        """Return less than comparison between this diference job and another.
        
        Args:
            other(:obj:DifferenceJob): The comparison difference job.
            
        Returns:
            bool: True if this difference job has a strictly lower difference
                (weight - runtime) than the other difference job or if they have
                equal differences but this job has a strictly lower weight.
                False otherwise.
        """
        return (
            self.difference < other.difference or (
                self.difference == other.difference
                and self.weight < other.weight
            )
        )
        
    def __str__(self):
        """Return a string representation.
        
            Returns:
                str: A string in the format (weight, runtime)
        """
        return "(" + str(self.__weight) + "," +  str(self.__runtime) + ")"
        
    def __repr__(self):
        """Return a string representation.
        
            Identical to str(self).
        
            Returns:
                str: A string in the format (weight, runtime)
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
#   Stanford Algorithms Specialization on Coursera
#   Course 03
#   Week 01 - Programming Assignment - Part 2: Ratio Schedule
#
#   2017-08-05
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from sortedcontainers import SortedList
from functools import total_ordering

@total_ordering
class RatioJob (object):
    """A single job for use in a ratio schedule.
    
    Intended only to achieve the outcomes required for the programming
    assignment in week one (1) of course three (3) of the Stanford Algorithms
    Specialization offered through Coursera.
    """
    def __init__(self, weight = 1, runtime = 1):
        """Instantiate a ratio job with weight and runtime.
        
        Args:
            weight (int): Value for completing the job. Defaults to one (1).
            runtime (int): Time required to complete the job once started.
                Defaults to one (1).
        
        Raises:
            TypeError: If either `weight` or `runtime` are not type `int`.
        """
        if type(weight) is not int:
            raise TypeError(
                "`weight` must have type `int`. Has type `" +
                str(type(weight)) + "`."
            )
        if type(runtime) is not int:
            raise TypeError("`runtime` must have type `int`. Has type `" +
                str(type(runtime)) + "`."
            )

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
    def ratio(self):
        """int: Calculated by dividing weight by runtime."""
        return float(self.weight) / float(self.runtime)
    
    def __eq__(self, other):
        """Return equality comparison between this ratio job and another.
        
        Args:
            other(:obj:`RatioJob`): The comparison ratio job.
        
        Returns:
            bool: True if this ratio job and the other have equal weight and
            runtime properties. False otherwise.
        """
        return self.weight == other.weight and self.runtime == other.runtime
    
    def __lt__(self, other):
        """Return less than comparison between this ratio job and another.
        
        Used in conjuction with equality comparison and @total_ordering to
        create all comparison methods.
        
        Args:
            other(:obj:RatioJob): The comparison ratio job.
            
        Returns:
            bool: True if this ratio job has a strictly lower ratio (weight /
                runtime) than the other ratio job or if they have equal
                ratios but this job has a strictly lower weight. False otherwise.
        """
        return (
            self.ratio < other.ratio or (
                self.ratio == other.ratio
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
        """Return a string inspection.
        
            Identical to str(self).
        
            Returns:
                str: A string in the format (weight, runtime)
        """
        return str(self)

class RatioSchedule (object):
    """A sorted list of ratio jobs.
    
    Intended only to achieve the outcomes required for the programming
    assignment in week one (1) of course three (3) of the Stanford Algorithms
    Specialization offered through Coursera.
    
    Attributes:
        __schedule(:obj:`SortedList` of :obj:`RatioJob`):
            List of ratio jobs sorted in ascending order.
    """
    def __init__(self, ascending = True, jobList = None):
        """Instantiate a ratio schedule with options job list.
        
        Args:
            ascending(bool, optional): Sort jobs in ascending order of 
                ratio (weight / runtime) if True, descending order if False.
        
            jobList(:obj:`list` of :obj:`RatioJob` or of :obj:`list`, optional):
                List of ratio jobs or list of lists, sorted or not, to include
                in the schedule. Each list in a list of list must include the
                job weight as the first element and the job runtime as the
                second element. Additional elements ignored.
            
        Raises:
            TypeError: If `ascending` not of type `bool` or if the optional job
                list includes an element not of type `RatioJob` or `list`.
            LookupError: If the any element in the optional job is of type
                `list` with length less than two (2).
        """
        self.__schedule = SortedList()
        if type(ascending) is bool: self.__ascending = ascending
        else:
            raise TypeError("`ascending` must have type `bool`. Found type `" +
                str(type(ascending)) + "`."
            )
        if jobList is not None: self.addJobList(jobList)
    
    @property
    def ascending(self):
        """bool: True if jobs sorted in ascending order by ratio (weight /
            length), False otherwise.
        """
        return self.__ascending
    
    @property
    def weightedRuntime(self):
        """int: Weighted runtime for all jobs in the schedule. Weighted runtime
            calculated for each job by multiplying the job's weight by its
            completion time (i.e., the sum of all preceding job runtimes plus
            the job's runtime).
            
        
        Calculated upon request in `O(n)` time where `n` is the number of jobs
        in the schedule.
        """
        rt, wrt = self.__calculateRuntimes()
        return wrt
    
    @property
    def runtime(self):
        """int: Un-Weighted runtime for all jobs in the schedule.
            
        Calculated upon request in `O(n)` time where `n` is the number of jobs
        in the schedule.
        """
        rt, wrt = self.__calculateRuntimes()
        return rt
    
    def __calculateRuntimes(self):
        """Calculate un-weighted and weighted runtimes.
        
        Internal method. Use `runtime` and `weightedRuntime` properties instead.
        
        Returns
            runtime(int): Un-weighted runtime for all jobs in the schedule.
            weightedRuntime(int): Weighted runtime for all jobs in the schedule.
                Weighted runtime calculated for each job by multiplying the
                job's weight by its completion time (i.e., the sum of all
                preceding job runtimes plus the job's runtime).
        """
        rt = 0
        wrt = 0
        jobs = iter(self.__schedule) if self.ascending else reversed(self.__schedule)
        for j in jobs:
            rt = rt + j.runtime
            wrt = wrt + rt * j.weight
        return rt, wrt

    def addJob(self, job):
        """Add one ratio job to the schedule.
        
        Args:
            job(:obj:`RatioJob`): The ratio job to add.
        
        Raises:
            TypeError: If the job is not of type `RatioJob`.
        """
        if type(job) is RatioJob: self.__schedule.add(job)
        else:
            raise TypeError("`job` must have type `RatioJob`. Has type `" +
                str(type(job)) + "`."
            )
    
    def createAndAddJob(self, weight, runtime):
        """Add one ratio job to the schedule.
        
        Args:
            weight(int): Value for completing the job.
            runtime(int): Time required to complete the job once started.
        """
        job = RatioJob(weight, runtime)
        self.addJob(job)

    def addJobList(self, jobList):
        """Add multiple ratop jobs from a list to the schedule.
        
        Args:
            jobList(:obj:`list` of :obj:`RatioJob` or of :obj:`list`, optional):
                List of ratio jobs or list of lists, sorted or not, to include
                in the schedule. Each list in a list of list must include the
                job weight as the first element and the job runtime as the
                second element. Additional elements ignored.

        Raises:
            TypeError: If the optional job list includes an element not of type
                `RatioJob` or `list`.
            LookupError: If the any element in the optional job is of type
                `list` with length less than two (2).
        """
        for j in jobList:
            if type(j) is RatioJob: self.addJob(j)
            elif type(j) is list: self.createAndAddJob(j[0], j[1])
            else:
                raise TypeError(
                    "All elements in the optional job list must have type" +
                    " `RatioJob` or `list`. Found instance of `" +
                    str(type(j)) + "`."
                )

    def __str__(self):
        """Return a string representation.
        
            Returns:
                str: A string listing the ratio jobs in sorted order.
        """
        jobs = iter(self.__schedule) if self.ascending else reversed(self.__schedule)
        return "[" + ",".join(map(lambda j: str(j), jobs)) + "]"
    
    def __repr__(self):
        """Return a string inspection.
        
            Returns:
                str: A string using the same format as repr(SortedList).
        """
        return repr(self.__schedule)
    
#
#   Main
#
# Instantiate schedule
schedule = RatioSchedule(ascending = False)

# Read jobs from jile
with open('jobs.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add job from each line
    for l in f:
        j = l.strip().split(" ")
        schedule.createAndAddJob(int(j[0]), int(j[1]))

# Calculate weighted runtime
print "Weighted Runtime:", schedule.weightedRuntime
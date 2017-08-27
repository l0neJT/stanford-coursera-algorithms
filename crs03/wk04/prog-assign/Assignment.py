#   Stanford Algorithms Specialization on Coursera
#   Course 03
#   Week 04 - Programming Assignment
#
#   2017-08-26
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from copy import copy, deepcopy
from functools import total_ordering

@total_ordering
class item:
    """A generic item with cost and value.
    
    Items can be compared and ordered.
    """
    def __init__(self, cost, value):
        """Create a single item with cost and value.
        
        Args:
            cost (int): The item cost.
            value (int): The value of the item.
        """
        if type(cost) is not int:
            raise TypeError("The item cost must be an integer. Has type &s." %\
                str(type(cost)))
        if type(value) is not int:
            raise TypeError("Parameter value must be an integer. Has type &s." %\
                str(type(value)))
        self.cost = cost
        self.value = value
    
    # @property
    # def cost(self):
    #     """int: The item cost."""
    #     return self.__cost
    
    # @cost.setter
    # def cost(self, cost):
    #     """Set the item cost.
        
    #     Args:
    #         cost (int): The item cost.
    #     """
    #     if type(cost) is not int:
    #         raise TypeError("The item cost must be an integer. Has type &s." %\
    #             str(type(cost)))
    #     self.__cost = cost
    
    # @property
    # def value(self):
    #     """int: The value of the item."""
    
    # @value.setter
    # def value(self, value):
    #     """Set the value of the item.
        
    #     Args:
    #         value (int): The value of the item.
    #     """
    #     if type(value) is not int:
    #         raise TypeError("Parameter value must be an integer. Has type &s." %\
    #             str(type(value)))
    #     self.__value = value
    
    def __eq__(self, other):
        """Compare this and another item for equality.
        
        Args:
            other(`obj`item): The other item for comparison.
        Returns:
            bool: True if items have equal value and cost. False otherwise.
        """
        return self.value == other.value and self.cost == other.cost
    
    def __lt__(self, other):
        """Determine if this item is strictly less than another item.
        
        Args:
            other(`obj`item): The other item for comparison.
        Returns:
            bool: True if this item has a lower ratio of value to cost. False
                otherwise.
        """
        return self.value * other.cost < other.value * self.cost or \
self.value * other.cost < other.value * self.cost and self.value < other.value
    
    def __copy__(self):
        """Return a new item with equal cost and value.
        
        Returns:
            `obj`item: The new item.
        """
        return type(self)(self.cost, self.value)

class knapsack:
    """A container for efficiently packing items.
    
    """
    
    def __init__(self, capacity, items = None, allowDuplicates = True):
        """Create a new knapsack with optional list of items to pack.
        
        Args:
            capacity(int): The maximum total cost of packed items.
            items(`obj`list of `obj`item, optional): Initial items for 
                eventual packing into the knapsack. Permits duplicate items.
            allowDuplicates(bool, optional): True to allow duplicate items. 
                False to ignore. Defaults to True.
        """
        if type(capacity) is not int:
            raise TypeError("The capcity must be an integer. Has type &s." %\
                str(type(capacity)))
        self.__capacity = capacity
        self.__packed = False
        self.__packedItems = []
        self.__packingList = []
        self.__allowDuplicates = allowDuplicates
        if items is not None:
            self.addItemsToPackingList(items)
    
    @property
    def allowDuplicates(self):
        """bool: Indicator if packing list can contain duplicate items."""
        return self.__allowDuplicates
    
    @property
    def capacity(self):
        """int: The maximum total cost of packed items."""
        return self.__capacity
    
    @property
    def countPackingListItems(self):
        """int: The count of items in the packing list."""
        return len(self.__packingList)
    
    @property
    def packed(self):
        """bool: Indicator if knapsack currently packed."""
        return self.__packed
    
    @property
    def packedItems(self):
        """`obj`list: of `obj`item: Items currently packed into the knapsack."""
        return deepcopy(self.__packedItems) if self.packed else []
    
    def addItemsToPackingList(self, items):
        """Add multiple items to the packing list.
        
        Args:
            items(`obj`list of `obj`item): List of items for eventual packing
                into the knapsack.
        """
        for i in items:
            self.createAndAddItemToPackingList(i.cost, i.value)
    
    def createAndAddItemToPackingList(self, cost, value):
        """Create and add a single item to the packing list.
        
        Args:
            cost (int): The item cost.
            value (int): The value of the item.
        """
        newI = item(cost, value)
        if self.allowDuplicates:
            self.__packingList.append(newI)
            self.__packed = False
        elif newI not in self.__packingList:
            self.__packingList.append(newI)
            self.__packed = False
    
    def pack(self):
        """Pack items to maximize value within the knapsack capacity.
        
        Returns:
            obj`list: of `obj`item: Items packed into the knapsack.
        """
        if not self.packed:
            # Initialize high and low partitions
            cost = 0
            value = 0
            self.__packedItems = []
            
            # Iterate from highest value:cost item to lowest
            for i in sorted(self.__packingList, reverse = True):
                if cost + i.cost <= self.capacity:
                    cost += i.cost
                    value += i.value
                    self.__packedItems.append(i)
                elif value < i.value or value == i.value and cost > i.cost:
                    cost = i.cost
                    value = i.value
                    items = [i]
            
            # Indicate knapsack packed
            self.__packed = True

        # Return list of packed items
        return self.packedItems

#
#   Main
#
# Open file
f = open("knapsack1.txt")

# Read first list to get capacity and initialize knapsack
l = next(f)
sack = knapsack(int(l.strip().split(" ")[0]))

# Read remaining lines to add items to packing list 
for l in f:
    i = l.strip().split(" ")
    sack.createAndAddItemToPackingList(int(i[1]), int(i[0]))

# Print information about knapsack
print "%s knapsack with %d capacity and %d items on the packing list." % \
    ("Packed" if sack.packed else "Unpacked", sack.capacity, \
    sack.countPackingListItems)
    
# Pack items
packedItems = sack.pack()

# Print information about packed items
print "Packed %d items with value %d and cost %d." % (len(packedItems), \
    reduce(lambda a, b: a + b, map(lambda i: i.value, packedItems)), \
    reduce(lambda a, b: a + b, map(lambda i: i.cost, packedItems)))
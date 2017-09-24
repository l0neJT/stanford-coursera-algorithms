#   Stanford Algorithms Specialization on Coursera
#   Course 04
#   Week 03 - Programming Assignment - Test SciPy
#
#   2017-09-23
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
from scipy.spatial.distance import pdist
import time


def squareToCondensed(i, j, n):
    """Returns the index of the element in a condensed distance matrix from its
        square distance matrix indices.
        
        Based on responses to https://stackoverflow.com/questions/13079563/how-does-condensed-distance-matrix-work-pdist
        
        Args:
            i (int): The first index from the square distance matrix.
            j (int): The second index from the square distance matrix.
            n (int): The lenght of the condensed distance matrix.
        
        Returns:
            int: The index of the element in a condensed distance matrix.
    """
    assert i != j, "No diagonal elements in condensed matrix."
    if i < j: i, j = j, i
    return n*j - j*(j + 1)/2 + i - 1 - j

def main():
    # Initialize empty node array
    nodes = []
    
    # Read nodes from file with euclidian x and y-coordinates
    with open('nn_10.txt', 'r') as f:
        # Skip first line
        next(f)
        
        # Create and add node from each line
        for l in f:
            nodes.append(map(lambda v: float(v), l.strip().split(" "))[1:])
        
    # Print nodes from list for debugging
    print "Graph with %d nodes. First ten:" % len(nodes)
    print nodes[:10]
    
    # Calculate pairwise distances
    dists = pdist(nodes, "euclidean")
    
    # Print pairwise distances for debugging
    print "Calculated %d distances." % len(dists)

if __name__ == "__main__":
    start = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start))
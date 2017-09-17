#   Stanford Algorithms Specialization on Coursera
#   Course 04
#   Week 02 - Programming Assignment - A Quick Scatter Plot
#
#   2017-09-16
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
import matplotlib
matplotlib.use('Agg')   # Needed to render in headless environment
import matplotlib.pyplot as plt

#
# Main
#
# x and y-axes
x = []
y = []

# Read nodes from file with euclidian x and y-coordinates
with open('tsp.txt', 'r') as f:
    # Skip first line
    next(f)
    
    # Create and add edge from each line
    for l in f:
        n = l.strip().split(" ")
        x.append(n[0])
        y.append(n[1])

# print x, y
plt.scatter(x, y)
plt.savefig("tsp-ScatterPlot.svg")
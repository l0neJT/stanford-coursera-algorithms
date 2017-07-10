#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 01 - Programming Assignment - Order SCC
#
#   2017-07-09
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
import json

scc = json.load(open('SCC.json', 'r'))
limitTop = 5
topSCC = [0] * 5
minLen = 0

for k in scc.keys():
    thisLen = len(scc[k])
    for i in xrange(0, limitTop):
        if thisLen >= topSCC[i]:
            topSCC.insert(i, thisLen)
            topSCC.pop()
            break

print topSCC

# maxKey = ''
# maxLen = 0
# for k in scc.keys():
#     if len(scc[k]) > maxLen:
#         maxKey = k
#         maxLen = len(scc[k])

# print maxKey
# print maxLen
# print len(set(scc[maxKey]))
# print scc[maxKey][:1000]

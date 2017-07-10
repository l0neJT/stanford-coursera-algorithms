#   Stanford Algorithms Specialization on Coursera
#   Course 02
#   Week 01 - Programming Assignment - Order SCC
#
#   2017-07-09
#   Logan J Travis
#   loganjtravis@gmail.com

# Imports
import json

scc = json.load(open('SCC_InstructorTest01.json', 'r'))
topSCC = [0]
limitTop = 10
minLen = 0

for k in scc.keys():
    thisLen = len(set(scc[k]))
    if thisLen > minLen:
        topSCC.append(thisLen)
        if len(topSCC) > limitTop:
            topSCC.remove(minLen)
            minLen = min(topSCC)

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
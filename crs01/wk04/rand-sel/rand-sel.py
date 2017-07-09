#   Stanford Algorithms Specialization on Coursera
#   Course 01
#   Week 04 - Random Selection
#
#   2017-07-01
#   Logan J Travis
#   loganjtravis@gmail.com

import random

def partIntArr(arr, start, length):
    rndPos = random.randrange(start, start + length - 1)
    arr[start], arr[rndPos] = arr[rndPos], arr[start]
    pvtVal = arr[start];
    gtPos = start + 1;
        
    for i in xrange(gtPos, gtPos + length - 1):
        if arr[i] < pvtVal:
            arr[gtPos], arr[i] = arr[i], arr[gtPos]
            gtPos += 1
    
    pvtPos = gtPos - 1
    arr[start], arr[pvtPos] = arr[pvtPos], arr[start]
    
    return pvtPos
    
def quickSortIntArr(arr, start, length):
    if length <= 1:
        return 0
    
    pvtPos = partIntArr(arr, start, length)
    lftLen = pvtPos - start
    lftComp = quickSortIntArr(arr, start, lftLen)
    rgtComp = quickSortIntArr(arr, pvtPos + 1, length - lftLen - 1)
    
    return length - 1 + lftComp + rgtComp
    
def rSelectIntArr(arr, start, length, iStat):
    if length <= 1:
        return arr[start]
    
    pvtPos = partIntArr(arr, start, length)
    lftLen = pvtPos - start
    if pvtPos == iStat - 1:
        return arr[pvtPos]
    elif pvtPos > iStat - 1:
        return rSelectIntArr(arr, start, lftLen, iStat)
    else:
        return rSelectIntArr(arr, pvtPos + 1, length - lftLen - 1, iStat)
    



f = open('QuickSort.txt', 'r')
arr = map(lambda s: int(s.strip()) if s else 0, list(f))
print rSelectIntArr(arr, 0, len(arr), 7499)
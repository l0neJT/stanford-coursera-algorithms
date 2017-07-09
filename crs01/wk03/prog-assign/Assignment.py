#   Stanford Algorithms Specialization on Coursera
#   Course 01
#   Week 03 - Programming Assignment
#
#   2017-06-25
#   Logan J Travis
#   loganjtravis@gmail.com

def makeInt(s):
    s = s.strip()
    return int(s) if s else 0

def partIntArr(arr, start, length):
    firstVal = arr[start]
    lastVal = arr[start + length - 1]
    midPos = start + (length + 1) // 2 - 1
    midVal = arr[midPos]
    
    if (midVal < lastVal and midVal >= firstVal) or (midVal > lastVal and midVal <= firstVal):
        arr[start], arr[midPos] = arr[midPos], arr[start]
    if (lastVal < midVal and lastVal > firstVal) or (lastVal > midVal and lastVal < firstVal):
        arr[start], arr[start + length - 1] = arr[start + length - 1], arr[start]

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



f = open('QuickSort.txt', 'r')
arr = map(makeInt, list(f))
print quickSortIntArr(arr, 0, len(arr))
print arr[:100]
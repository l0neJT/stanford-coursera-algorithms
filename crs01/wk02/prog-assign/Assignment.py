#   Stanford Algorithms Specialization on Coursera
#   Course 01
#   Week 02 - Programming Assignment
#
#   2017-06-11
#   Logan J Travis
#   loganjtravis@gmail.com

def makeInt(s):
    s = s.strip()
    return int(s) if s else 0
    
def mergeSort(arr, i):
    lenArr = len(arr)
    sortArr = []
    # print "In:" + str(arr)
    
    if lenArr == 1 : sortArr = arr
    else:
        split = lenArr // 2
        
        sortArrLft, iLft = mergeSort(arr[:split], i)
        sortArrRgt, iRgt = mergeSort(arr[split:], i)
        # print arr[:split], iLft, sortArrLft
        # print arr[split:], iRgt, sortArrRgt
        # print '---'
        i = iLft + iRgt

        
        for n in xrange(lenArr):
            if len(sortArrLft) == 0:
                sortArr.extend(sortArrRgt)
                break
            if len(sortArrRgt) == 0:
                sortArr.extend(sortArrLft)
                break
            
            if sortArrLft[0] <= sortArrRgt[0]: sortArr.append(sortArrLft.pop(0))
            else:
                sortArr.append(sortArrRgt.pop(0))
                i += len(sortArrLft)
    
    # print "Out: " + str(sortArr)    
    return sortArr, i
        
        

f = open('IntegerArray_TEST.txt', 'r')
arr = map(makeInt, list(f))
sortArr, i = mergeSort(arr, 0)
print arr
print sortArr
print i
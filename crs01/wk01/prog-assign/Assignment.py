#   Stanford Algorithms Specialization on Coursera
#   Course 01
#   Week 01 - Programming Assignment
#
#   2017-05-28
#   Logan J Travis
#   loganjtravis@gmail.com

from math import ceil, log10

#
def makeInt(s):
    s = s.strip()
    return int(s) if s else 0

#   
def karatMulti(a, b):
    #   Zero Case
    if (a == 0 or b == 0):
        return 0
    
    #   Base Case
    elif (a < 10 and b < 10):
        return a * b
    
    #   Recursive Case
    else:
        #   Convert a and b to strings
        aStr = str(a)
        bStr = str(b)
        
        #   Calculate max number of digits from a and b
        m = max(len(aStr), len(bStr))
        
        #   Divide by two (integer) to get split
        split = m // 2
        
        #   Split a and b
        #
        #   NOTE: Uses negative indices to split from right to left.
        aHi = makeInt(aStr[:-split])
        aLo = makeInt(aStr[-split:])
        bHi = makeInt(bStr[:-split])
        bLo = makeInt(bStr[-split:])
        
        #   Recursively call Karatsuba multiplication to determine components
        z2 = karatMulti(aHi, bHi)
        z0 = karatMulti(aLo, bLo)
        z1 = karatMulti((aHi + aLo), (bHi + bLo)) - z2 - z0
        
        #   Return sum
        return z2 * pow(10, 2 * split) + z1 * pow(10, split) + z0

a = 3141592653589793238462643383279502884197169399375105820974944592
b = 2718281828459045235360287471352662497757247093699959574966967627

print karatMulti(a, b)
print a * b
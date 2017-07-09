#   Stanford Algorithms Specialization on Coursera
#   Course 01
#   Week 01 - Programming Assignment (binary)
#
#   2017-06-01
#   Logan J Travis
#   loganjtravis@gmail.com

#   Katarsuba multiplication implemented in base 2
def karatMulti(a, b):
    #   Get bit length (highest non-zero bit) for a and b
    aBLen = a.bit_length()
    bBLen = b.bit_length()
    
    #   Zero Case
    if (a == 0 or b == 0):
        return 0
    
    #   Base Case
    elif (aBLen == 1 and bBLen == 1):
        return a & b
    
    #   Recursive Case
    else:
        #   Calculate maximum bit length for a and b
        m = max(aBLen, bBLen)
        
        #   Divide by two (floor) to get split
        split = m // 2
        
        #   Create remainder mask, the binary number represented by a series of
        #   1s length split
        remain = (1 << split) - 1
        
        #   Split a and b
        aHi = a >> split
        aLo = a & remain
        bHi = b >> split
        bLo = b & remain
        
        #   Recursively call Karatsuba multiplication to determine components
        z2 = karatMulti(aHi, bHi)
        z0 = karatMulti(aLo, bLo)
        z1 = karatMulti((aHi + aLo), (bHi + bLo)) - z2 - z0
        
        #   Return sum; more commonly written:
        #   z2 * 2^(2 * split) + z1 * 2^split + z0
        return (z2 << (split << 1)) + (z1 << split) + z0

a = 3141592653589793238462643383279502884197169399375105820974944592
b = 2718281828459045235360287471352662497757247093699959574966967627

print karatMulti(a, b)
print a * b
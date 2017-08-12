from itertools import combinations

def generateMasks(n, upToK):
    masks = [0]
    for k in xrange(1, upToK + 1):
        for c in combinations(range(n), k):
            masks.append(reduce(lambda acc, v: acc + pow(2, v), c))
    return set(masks)

print generateMasks(4, 2)
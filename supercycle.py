import numpy as np 
import math

import split

def get_shuffled_range(start, count) :
        ix = list(range(start,start+count))
        np.random.shuffle(ix)
        return ix

def initialize_indexes(counts) :
    indexes = []
    bases = []
    sum = 0
    for c in counts :
        ix = get_shuffled_range(sum, c)
        indexes.append(ix)

        bases.append(sum)
        sum += c

    return indexes, bases

def extend_index(stub, base, count, hold) :
    rest = get_shuffled_range(base, count)
    tail = []
    while len(stub) < hold and rest :
        r = rest[0]
        if r in stub :
            tail.append(r)
        else :
            stub.append(r)
        rest = rest[1:]

    stub.extend(tail)       
    stub.extend(rest)

    return stub

def supercycle(count, tiers, per_tier) :
    count_per_tier = split.make_tier_counts(count, tiers, per_tier)
    print('counts', count_per_tier)

    indexes, bases = initialize_indexes(count_per_tier)
    rows = int(math.ceil(max(count_per_tier)/per_tier))
    print(rows)
    for _ in range(rows) :
        row_index = []
        for i in range(len(indexes)) :
            ix = indexes[i]
            if len(ix) < per_tier :
                ix = extend_index(ix, bases[i], count_per_tier[i], per_tier)

            t = ix[:per_tier]
            u = ix[per_tier:]
            row_index.extend(t)
            indexes[i] = u
        
        row_index.sort()
        print(row_index)

if __name__ == '__main__' :
    count = 3592
    supercycle(count, 5, 2)
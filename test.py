import split
import splitutils
import merge

import numpy as np

def compute_dq(seq) :
    diffs = [i - seq[i] for i in range(len(seq))]
    dq = sum([diff*diff for diff in diffs])
    #dq = sum([abs(x) for x in t])

    return dq #// 2

def print_state(seq, dq) :
    print(dq, seq)

def next_state(seq, spread) :
    indexes = split.choose_indexes(len(seq), spread, 10)
    subset, remainder = splitutils.partition_by_index(seq, indexes)
    subset.sort()
    t = merge.merge_data(remainder, subset, indexes)
    return t

def unstall(seq, dq) :
    for start in range(0, len(seq), 5) :
        stop = min(len(seq), start+10)
        indexes = list(range(start, stop))
        subset, remainder = splitutils.partition_by_index(seq, indexes)
        subset.sort()
        seq = merge.merge_data(remainder, subset, indexes)

        temp_dq = compute_dq(seq)
        if temp_dq < dq :
            return seq, temp_dq

def dotest() :
    nums = list(range(100))
    np.random.shuffle(nums)

    last_dq = compute_dq(nums)
    dq_count = 1
    print_state(nums, last_dq)

    spread = len(nums)

    while True :
        nums = next_state(nums, spread)

        dq = compute_dq(nums)
        if dq == last_dq :
            dq_count += 1
        else :
            last_dq = dq
            dq_count = 1

        if dq_count > 10 :
            print("Stalled, unstalling...")
            nums, dq = unstall(nums, dq)
            last_dq = dq
            dq_count = 0
        else :
            print_state(nums, dq)
            if dq == 0 :
                break

if __name__ == '__main__' :
    dotest()
    print(splitutils.make_geometric_series(3592, 7, 2, 2.0))
    print(splitutils.make_geometric_series(3592, 7, 2, 1.5))
    print(splitutils.make_geometric_series(3592, 7, 2, 1.0))
    print(splitutils.make_geometric_series(3592, 7, 2, 0.5))
    print(splitutils.make_geometric_series(3592, 7, 2, 0.0))
    print(splitutils.make_geometric_series(3592, 7, 2, -2))
    print(splitutils.make_geometric_series(3592, 7, 2, 4.2))

import sys

import numpy as np

import supercycle

def get_data(fname):
    with open(fname) as fh:
        return fh.readlines()

def get_subset_from_range(rmin, rmax, count) :
    r = range(rmin, rmax)
    if len(r) < count :
        return list(r)

    s = list(np.random.choice(r, size=count, replace=False))
    return s

def choose_indexes(len, spread, count):
    if len <= count :
        return list(range(len))

    spread = max(min(len, spread), count)
    maxbase = len - spread
    base = 0
    if maxbase > base :
        np.random.randint(0, maxbase+1)

    indexes = get_subset_from_range(base, base+spread, count)
    indexes.sort()
    return indexes

def choose_indexes_by_stride(len, count) :
    width = len // count
    basemax = len - 1 - (count -1) * width
    base = np.random.randint(0, basemax+1)
    indexes = [base + i * width for i in range(count)]
    return indexes

def make_tier_counts(count, parts, floor):
    if count <= 0:
        return [0] * parts
    if parts == 0:
        return []
    if parts == 1:
        return [count]

    divisor = 2 ** parts
    part = count // divisor
    if part < floor:
        part = floor

    tail = make_tier_counts(count - part, parts - 1, floor * 2)

    value = [part] + tail
    return value

def count_to_index(counts) :
    start = 0
    indexes = []

    for c in counts :
        end = start + c
        ix = (start, end)
        indexes.append(ix)
        start += c

    return indexes

def choose_indexes_by_tier(item_count, tiers, per_tier) :
    tier_counts = make_tier_counts(item_count, tiers, 1)
    if item_count == 0 or tiers <= 0 or len(tier_counts) == 0 or tier_counts[-1] <= 0:
        return choose_indexes_by_stride(item_count, tiers * per_tier)

    index_ranges = count_to_index(tier_counts)
    indexes = []
    for l, h in index_ranges:
        t = get_subset_from_range(l, h, 2)
        indexes.extend(t)

    indexes.sort()
    return indexes

def choose_indexes_by_tier_state(fname, tiers, per_tier) :
    state = supercycle.SupercycleState(fname)
    if not state.is_valid():
        state.initialize(tiers, per_tier)

    indexes = state.next()
    state.write_state()
    return indexes

def split_by_indexes(data, indexes):
    subset = [data[i] for i in range(len(data)) if i in indexes]
    remainder = [data[i] for i in range(len(data)) if i not in indexes]
    return subset, remainder

def write_subset(fname, subset, indexes):
    with open(fname + '.out', 'w') as fh:
        fh.write('# ')
        fh.write(' '.join([str(i) for i in indexes]))
        fh.write('\n')

        fh.write(''.join(subset))

def write_remainder(fname, data):
    with open(fname + '.rem', 'w') as fh:
        fh.write(''.join(data))

def split(fname, strategy):
    data = get_data(fname)

    n = len(data)
    indexes = strategy(n)

    subset, remainder = split_by_indexes(data, indexes)

    write_subset(fname, subset, indexes)
    write_remainder(fname, remainder)

if __name__ == '__main__':
    fname = 'numbers.dat'
    def strategy(n) :
        #return choose_indexes_by_stride(n, 10)
        #return choose_indexes_by_tier(n, 5, 2)
        return choose_indexes_by_tier_state(fname, 5, 2)

    if len(sys.argv) > 1 :
        fname = sys.argv[1]

    split(fname, strategy)

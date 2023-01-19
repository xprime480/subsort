import sys
import math

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

def compute_tier_sizes(number_of_items, number_of_tiers, minimum_for_first_tier, tier_size_ratio=2.0):
    if number_of_items <= 0:
        return [0] * number_of_tiers
    if number_of_tiers == 0:
        return []
    if number_of_tiers == 1:
        return [number_of_items]

    divisor = number_of_tiers
    if tier_size_ratio != 1 :
        divisor = (tier_size_ratio ** number_of_tiers - 1) / (tier_size_ratio - 1)
    number_for_first_tier = math.floor(number_of_items // divisor)
    if number_for_first_tier < minimum_for_first_tier:
        number_for_first_tier = min(number_of_items, minimum_for_first_tier)

    number_of_items -= number_for_first_tier
    number_of_tiers -= 1
    minimum_for_first_tier = math.ceil(minimum_for_first_tier * tier_size_ratio)
    tail = compute_tier_sizes(number_of_items, number_of_tiers, minimum_for_first_tier, tier_size_ratio)

    value = [number_for_first_tier] + tail
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

def choose_indexes_by_tier(number_of_items, number_of_tiers, per_tier) :
    tier_sizes = compute_tier_sizes(number_of_items, number_of_tiers, 1)
    if number_of_items == 0 or number_of_tiers <= 0 or len(tier_sizes) == 0 or tier_sizes[-1] <= 0:
        return choose_indexes_by_stride(number_of_items, number_of_tiers * per_tier)

    index_ranges = count_to_index(tier_sizes)
    indexes = []
    for l, h in index_ranges:
        t = get_subset_from_range(l, h, 2)
        indexes.extend(t)

    indexes.sort()
    return indexes

def choose_indexes_by_tier_state(fname, number_of_tiers, total_count) :
    state = supercycle.SupercycleState(fname, number_of_tiers, total_count)
    indexes = state.next()
    state.write_state()
    return indexes

def split_by_indexes(data, indexes):
    subset = [data[i] for i in range(len(data)) if i in indexes]
    remainder = [data[i] for i in range(len(data)) if i not in indexes]
    return subset, remainder

def write_chosen(fname, subset, indexes):
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

    chosen, remainder = split_by_indexes(data, indexes)

    write_chosen(fname, chosen, indexes)
    write_remainder(fname, remainder)

if __name__ == '__main__':
    fname = 'numbers.dat'
    def strategy(n) :
        #return choose_indexes_by_stride(n, 10)
        #return choose_indexes_by_tier(n, 5, 2)
        return choose_indexes_by_tier_state(fname, 7, 10)

    if len(sys.argv) > 1 :
        fname = sys.argv[1]

    split(fname, strategy)

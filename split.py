import sys

import numpy as np

def get_data(fname):
    with open(fname) as fh:
        return fh.readlines()

def choose_indexes(len, spread, count):
    if len <= count :
        return list(range(len))

    spread = max(min(len, spread), count)
    maxbase = len - spread
    base = 0
    if maxbase > base :
        np.random.randint(0, maxbase+1)
    all = list(range(base, base+spread))

    indexes = list(np.random.choice(all, size=count, replace=False))
    indexes.sort()
    return indexes

def choose_indexes_by_stride(len, count) :
    width = len // count
    basemax = len - 1 - (count -1) * width
    base = np.random.randint(0, basemax+1)
    indexes = [base + i * width for i in range(count)]
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
        return choose_indexes_by_stride(n, 10)

    if len(sys.argv) > 1 :
        fname = sys.argv[1]

    split(fname, strategy)

import sys

import numpy as np 
import math

import split

class SupercycleState(object) :
    def __init__(self, fname, number_of_tiers, total_count):
        self.fname = fname
        self.tiers = number_of_tiers
        self.compute_per_tier(number_of_tiers, total_count)
        self.read_old_state()
        self.make_state_from_data()

    def compute_per_tier(self, number_of_tiers, total_count) :
        count_per_tier = []
        for _ in range(number_of_tiers) :
            if total_count <= 0 :
                count_per_tier.append(0)
            else :
                this_tier_count = math.ceil(total_count / number_of_tiers)
                number_of_tiers -= 1
                total_count -= this_tier_count
                count_per_tier.append(this_tier_count)
        self.count_per_tier = count_per_tier

    def make_state_from_data(self) :
        self.reinitialize()
        self.initialize_indexes()

    def reinitialize(self) :
        data = split.get_data(self.fname)
        self.data = [v.rstrip() for v in data]
        count = len(data)

        self.tier_sizes = split.compute_tier_sizes(count, self.tiers, self.count_per_tier[0])
        self.initialize_bases()

        self.exclusions.intersection_update(set(self.data))

    def initialize_bases(self) :
        bases = []
        sum = 0
        for c in self.tier_sizes:
            bases.append(sum)
            sum += c
        self.bases = bases

    def initialize_indexes(self):
        indexes = []
        sum = 0

        for c in self.tier_sizes:
            ix = [i for i in get_shuffled_range(sum, c) if not self.is_excluded(i)]
            indexes.append(ix)
            sum += c

        self.indexes = indexes

    def read_old_state(self) :
        try :
            self.exclusions = set([x.rstrip() for x in split.get_data(self.fname + '.state')])
            self.exclusions.difference_update(set(['']))
        except Exception as ex :
            print('Unable to open statefile', ex)
            self.exclusions = set()

    def is_excluded(self, index) :
        data = self.data[index]
        return data in self.exclusions

    def write_state(self) :
        with open(self.fname + '.state', 'w') as fh :
            for e in self.exclusions :
                fh.write(e)
                fh.write('\n')

    def next(self) :
        indexes = self.indexes
        per_tier = self.count_per_tier

        row_index = []
        for i in range(len(indexes)) :
            needed = per_tier[i]
            ix = indexes[i]
            if len(ix) < needed :
                ix = self.extend_index(ix, i, needed)

            t = ix[:needed]
            row_index.extend(t)

            u = ix[needed:]
            indexes[i] = u

        self.add_to_exclusions(row_index)
        row_index.sort()
        return row_index

    def extend_index(self, stub, index, needed):
        rest = get_shuffled_range(self.bases[index], self.tier_sizes[index])
        self.delete_from_exclusions(rest)
        tail = []
        while len(stub) < needed and rest:
            r = rest[0]
            if r in stub:
                tail.append(r)
            else:
                stub.append(r)
            rest = rest[1:]

        stub.extend(tail)
        stub.extend(rest)

        return stub

    def add_to_exclusions(self, indexes) :
        data = set([self.data[i] for i in indexes])
        self.exclusions.update(data)

    def delete_from_exclusions(self, indexes) :
        data = set([self.data[i] for i in indexes])
        self.exclusions.difference_update(data)

def get_shuffled_range(start, count) :
        ix = list(range(start,start+count))
        np.random.shuffle(ix)
        return ix

if __name__ == '__main__' :
    fname = 'numbers.dat'
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    count = 0
    if len(sys.argv) > 2 :
        count = int(sys.argv[2])

    state = SupercycleState(fname, 5, 7)

    for _ in range(count) : 
        sample = state.next()
        print(sample)
    state.write_state()

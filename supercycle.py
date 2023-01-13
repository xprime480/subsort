import sys

import numpy as np 
import math

import split

class SupercycleState(object) :
    def __init__(self, fname, tiers, per_tier):
        self.fname = fname
        self.tiers = tiers
        self.per_tier = per_tier
        self.read_old_state()
        self.make_state_from_data()

    def make_state_from_data(self) :
        self.reinitialize()
        self.initialize_indexes()

    def reinitialize(self) :
        data = split.get_data(self.fname)
        dtemp = [(i, s.rstrip()) for i, s in enumerate(data)]
        self.base_data = [v for _,v in dtemp]
        self.index_to_data = dict(dtemp)
        count = len(data)

        count_per_tier = split.make_tier_counts(count, self.tiers, self.per_tier)
        self.count_per_tier = count_per_tier
        self.initialize_bases()

        self.exclusions.intersection_update(set(self.base_data))

    def initialize_bases(self) :
        bases = []
        sum = 0
        for c in self.count_per_tier:
            bases.append(sum)
            sum += c
        self.bases = bases

    def initialize_indexes(self):
        indexes = []
        alt_indexes = []
        sum = 0

        for c in self.count_per_tier:
            ix = [i for i in get_shuffled_range(sum, c) if not self.is_excluded(i)]
            alt_ix = [(i, self.index_to_data[i]) for i in ix]
            indexes.append(ix)
            alt_indexes.append(alt_ix)
            sum += c

        self.indexes = indexes
        self.alt_indexes = alt_indexes

    def read_old_state(self) :
        try :
            self.exclusions = set([x.rstrip() for x in split.get_data(self.fname + '.state')])
            self.exclusions.difference_update(set(['']))
        except Exception as ex :
            print('Unable to open statefile', ex)
            self.exclusions = set()

    def is_excluded(self, index) :
        data = self.index_to_data[index]
        return data in self.exclusions

    def write_state(self) :
        with open(self.fname + '.state', 'w') as fh :
            for e in self.exclusions :
                fh.write(e)
                fh.write('\n')

    def is_valid(self) :
        return self._valid

    def next(self) :
        indexes = self.indexes
        per_tier = self.per_tier

        row_index = []
        for i in range(len(indexes)):
            ix = indexes[i]
            if len(ix) < per_tier:
                ix = self.extend_index(ix, i)

            t = ix[:per_tier]
            row_index.extend(t)

            u = ix[per_tier:]
            indexes[i] = u

        self.add_to_exclusions(row_index)
        row_index.sort()
        return row_index

    def extend_index(self, stub, index):
        rest = get_shuffled_range(self.bases[index], self.count_per_tier[index])
        self.delete_from_exclusions(rest)
        tail = []
        while len(stub) < self.per_tier and rest:
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
        data = set([self.index_to_data[i] for i in indexes])
        self.exclusions.update(data)

    def delete_from_exclusions(self, indexes) :
        data = set([self.index_to_data[i] for i in indexes])
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

    state = SupercycleState(fname, 5, 2)

    for _ in range(count) : 
        sample = state.next()
        print(sample)
    state.write_state()

import sys
import itertools

import numpy as np 

import splitutils
import splitdata

class SupercycleState(object) :
    def __init__(self, dao, number_of_tiers, total_count):
        self.dao = dao

        self.dao.log('Creating SuperCycleState with parameters number_of_tiers: {0}, total_count: {1}'.format(number_of_tiers, total_count))

        self.read_old_state()
        self.data = self.dao.get_data()
        self.dao.log('Data length = {0}'.format(len(self.data)))

        self.compute_tier_data(number_of_tiers, total_count)
        self.dao.log('Computed tier parameters: count_per_tier: {0} tier_sizes: {1} adjusted number_of_tiers: {2}'.format(self.count_per_tier, self.tier_sizes, self.tiers))

        self.bases = list(itertools.accumulate([0] + self.tier_sizes[:-1]))
        self.exclusions.intersection_update(set(self.data))
        self.initialize_indexes()

    def compute_tier_data(self, number_of_tiers, total_count) :
        data_len = len(self.data)
        while number_of_tiers > 0 :
            count_per_tier = splitutils.make_geometric_series(total_count, number_of_tiers, 1, 1.0)
            tier_sizes = splitutils.make_geometric_series(data_len, number_of_tiers, count_per_tier[0], 1.618)
            if 0 not in tier_sizes :
                break
            number_of_tiers -= tier_sizes.count(0)

        self.tiers = number_of_tiers
        self.count_per_tier = count_per_tier
        self.tier_sizes = tier_sizes

    def initialize_indexes(self):
        indexes = []
        sum = 0

        for c in self.tier_sizes:
            ix = [i for i in get_shuffled_range(sum, c) if not self.is_excluded(i)]
            indexes.append(ix)
            sum += c

        self.indexes = indexes

    def is_excluded(self, index) :
        data = self.data[index]
        return data in self.exclusions

    def read_old_state(self):
        try:
            self.exclusions = set(self.dao.get_state())
            self.exclusions.difference_update(set(['']))
        except Exception as ex:
            print('Unable to open statefile', ex)
            self.exclusions = set()

    def write_state(self):
        self.dao.set_state(self.exclusions)

    def next(self) :
        indexes = self.indexes
        per_tier = self.count_per_tier

        self.dao.log('Initial index sizes: {0}'.format([len(ix) for ix in indexes]))

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
        self.dao.log('Extending index {0} ({1} - {2})'.format(index, self.bases[index], self.bases[index] + self.tier_sizes[index]))
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

    dao = splitdata.SplitData(fname)
    state = SupercycleState(dao, 5, 7)

    for _ in range(count) : 
        sample = state.next()
        print(sample)
    state.write_state()

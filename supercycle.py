import sys
import itertools
import math

import numpy as np 

import splitutils
import splitdata
import splitconfig

class SupercycleState(object) :
    def __init__(self, dao, config):
        self.dao = dao
        self.config = config

        self.read_old_state()
        self.data = self.dao.get_data()
        self.using_raw_indexes = False

        indexes = config.list_of_int_or_default('indexes', [])
        indexes = [i for i in indexes if i >= 0 and i < len(self.data)]
        indexes = list(set(indexes))
        if indexes :
            self.dao.log('Creating SuperCycleState with stipulated indexes {0}'.format(indexes))
            self.indexes = indexes
            self.using_raw_indexes = True
            return

        number_of_tiers = config.int_or_default('tier_count', 10)
        item_count = config.int_or_default('item_count', 10)
        offset = config.float_or_default('offset', 0)
        window = config.float_or_default('window', 0)

        self.dao.log('Creating SuperCycleState with parameters number_of_tiers: {0}, total_count: {1}, offset: {2}, window: {3}'.format(number_of_tiers, item_count, offset, window))

        item_count = self.compute_window(offset, window, item_count)
        self.dao.log('Data length = {0}, effective offset = {1}, effective window = {2}'.format(len(self.data), self.offset, self.window))

        self.compute_tier_data(number_of_tiers, item_count)
        self.dao.log('Computed tier parameters: count_per_tier: {0} tier_sizes: {1} adjusted number_of_tiers: {2}'.format(self.count_per_tier, self.tier_sizes, self.tiers))

        self.bases = [self.offset + i for i in itertools.accumulate([0] + self.tier_sizes[:-1])]
        self.exclusions.intersection_update(set(self.data))
        self.initialize_indexes()

    def compute_window(self, offset, window, total_count) :
        length = len(self.data)
        if total_count > length :
            total_count = length

        if 0 < window <= 1 :
            window *= length
        elif window > length or window <= 0:
            window = length
        elif window < total_count :
            window = total_count
        window = math.floor(window)

        if 0 < offset <= 1 :
            offset *= length
            offset = math.floor(offset)
        offset = max(0, min(length - window, offset))
        offset = math.floor(offset)

        self.window = window
        self.offset = offset

        return total_count

    def compute_tier_data(self, number_of_tiers, total_count) :
        data_len = self.window

        tier_sizes = self.config.list_of_int_or_default('tier_sizes', [])
        count_per_tier = self.config.list_of_int_or_default('count_per_tier', [])
        if tier_sizes and count_per_tier :
            # no sanity checking, assume the user has all their marbles
            temp_total_size = sum(tier_sizes)
            temp_total_count = sum(count_per_tier)
            remainder_total_size = total_count - temp_total_count
            remainder_total_count = data_len - temp_total_size
            if remainder_total_count > 0 and remainder_total_size > 0 :
                tier_sizes.append(remainder_total_count)
                count_per_tier.append(remainder_total_size)

            self.tiers = len(tier_sizes)
            self.tier_sizes = tier_sizes[:]
            self.count_per_tier = count_per_tier[:]

            return


        tier_ratio = self.config.float_or_default('tier_ratio', 1.618)
        first_tier_min = self.config.int_or_default('first_tier_min', 1)
        while number_of_tiers > 0 :
            count_per_tier = splitutils.make_geometric_series(total_count, number_of_tiers, 1, 1.0)
            first_tier_min_tmp = max(first_tier_min, count_per_tier[0])
            tier_sizes = splitutils.make_geometric_series(data_len, number_of_tiers, first_tier_min_tmp, tier_ratio)
            if 0 not in tier_sizes :
                break
            number_of_tiers -= tier_sizes.count(0)

        self.tiers = number_of_tiers
        self.count_per_tier = count_per_tier
        self.tier_sizes = tier_sizes

    def initialize_indexes(self):
        indexes = []

        for x in range(len(self.tier_sizes)):
            ix = [i for i in get_shuffled_range(self.bases[x], self.tier_sizes[x]) if not self.is_excluded(i)]
            indexes.append(ix)

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
        if self.using_raw_indexes :
            row_index = self.indexes[:]
        else :
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

    def finalize(self) :
        self.write_state()

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

def get_dao(config) :
    return splitdata.get_dao(config)

def get_indexer(config, dao) :
    return SupercycleState(dao, config)

if __name__ == '__main__' :
    fname = 'numbers.config'
    if len(sys.argv) > 1:
        fname = sys.argv[1]


    config = splitconfig.SplitConfig(fname)
    dao = get_dao(config)
    state = SupercycleState(dao, config)

    count = config.int_or_default('test_count', 0)
    for _ in range(count) : 
        sample = state.next()
        print(sample)
    state.write_state()

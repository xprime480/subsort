import sys
import importlib

import numpy as np

import supercycle
import splitutils
import splitdata
import splitconfig

def choose_indexes(len, spread, count):
    if len <= count :
        return list(range(len))

    spread = max(min(len, spread), count)
    maxbase = len - spread
    base = 0
    if maxbase > base :
        np.random.randint(0, maxbase+1)

    indexes = splitutils.get_subset_from_range(base, base+spread, count)
    indexes.sort()
    return indexes

def choose_indexes_by_stride(len, count) :
    width = len // count
    basemax = len - 1 - (count -1) * width
    base = np.random.randint(0, basemax+1)
    indexes = [base + i * width for i in range(count)]
    return indexes

def choose_indexes_by_tier(number_of_items, number_of_tiers, per_tier) :
    tier_sizes = splitutils.make_geometric_series(number_of_items, number_of_tiers, 1)
    if number_of_items == 0 or number_of_tiers <= 0 or len(tier_sizes) == 0 or tier_sizes[-1] <= 0:
        return choose_indexes_by_stride(number_of_items, number_of_tiers * per_tier)

    index_ranges = splitutils.compute_ranges(tier_sizes)
    indexes = []
    for l, h in index_ranges:
        t = splitutils.get_subset_from_range(l, h, 2)
        indexes.extend(t)

    indexes.sort()
    return indexes

def split(dao, indexer):
    indexes = indexer.next()
    dao.log('Split indexes: {0}'.format(indexes))
    included, excluded = splitutils.partition_by_index(dao.get_data(), indexes)
    dao.log('Split data: {0}'.format(included))

    dao.set_included(included, indexes)
    dao.set_excluded(excluded)
    indexer.finalize()

if __name__ == '__main__':
    fname = 'numbers.config'
    if len(sys.argv) > 1 :
        fname = sys.argv[1]

    config = splitconfig.SplitConfig(fname)
    if not config.is_ready() :
        print('Error reading config')
        sys.exit(1)

    package = config.get_or_default('package', '')
    if package :
        try :
            lib = importlib.import_module(package)
        except Exception as ex :
            print('Error importing pakage {0}: {1}'.format(package, ex))
            
        dao = lib.get_dao(config)
        indexer = lib.get_indexer(config, dao)
        split(dao, indexer)

    else :
        print('No valid package was specified, cannot split')


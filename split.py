import sys
import importlib
import math
import numpy as np

import splitutils
import splitconfig

def get_initial_data(dao, indexer) :
    indexes = indexer.next()
    data = dao.get_data()
    new = dao.get_new()
    excl = dao.get_excluded()
    return indexes, data, new, excl

def get_count(new, indexes) :
    if not new or len(indexes) == 0 :
        return 0
    #return min(len(indexes) // 2, int(math.ceil(len(new)/5)))
    return min(len(new), 5)

def get_temp_index(data, indexes) :
    lo = len(data) * 2 // 10
    hi = len(data) * 8 // 10
    temp = np.random.randint(lo, hi)
    while temp in indexes :
        temp += 1
    return temp

def update_data(indexes, data, new, excl, temp_index) :
    temp_data = new[0]

    if temp_index > len(data):
        indexes.append(len(data))
        data.append(temp_data)
    else:
        data.insert(temp_index, temp_data)
        new_indexes = [i if i < temp_index else i+1 for i in indexes]
        new_indexes.append(temp_index)
        new_indexes.sort()
        indexes = new_indexes

    excl.append(temp_data)
    new = new[1:]

    return indexes, data, new, excl

def set_data(dao, excl, new) :
    dao.set_excluded(excl)
    dao.set_new(new)

def get_data(dao, indexer) :
    indexes, data, new, excl = get_initial_data(dao, indexer)

    count = get_count(new, indexes)
    for _ in range(count) :
        temp_index = get_temp_index(data, indexes)
        indexes, data, new, excl = update_data(
            indexes, data, new, excl, temp_index)

    set_data(dao, excl, new)

    return data, indexes

def split(dao, indexer):
    data, indexes = get_data(dao, indexer)

    dao.log('Split indexes: {0}'.format(indexes))
    included, excluded = splitutils.partition_by_index(data, indexes)
    dao.log('Split data: {0}'.format(included))

    dao.set_included(included, indexes)
    dao.set_excluded(excluded)
    indexer.finalize()

def main(fname) :
    config = splitconfig.SplitConfig(fname)
    if not config.is_ready():
        print('Error reading config')
        sys.exit(1)

    package = config.get_or_default('package', '')
    if package:
        try:
            lib = importlib.import_module(package)
        except Exception as ex:
            print('Error importing pakage {0}: {1}'.format(package, ex))

        dao = lib.get_dao(config)
        indexer = lib.get_indexer(config, dao)
        split(dao, indexer)

    else:
        print('No valid package was specified, cannot split')

if __name__ == '__main__':
    fname = 'numbers.config'
    if len(sys.argv) > 1 :
        fname = sys.argv[1]
    main(fname)

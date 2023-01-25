import sys

import splitdata

def get_included(dao) :
    data = dao.get_included()

    indexline = data[0][2:]
    data = data[1:]

    indexes = [int(x) for x in indexline.split(' ')]

    return data, indexes

def merge_data(excluded, included, indexes) :
    indexes.sort()
    stop = min(len(included), len(indexes))
    for i in range(stop) :
        where = indexes[i]
        what = included[i]
        excluded.insert(where, what)
    
    return excluded

def merge(dao) :
    excluded = dao.get_excluded()
    included, indexes = get_included(dao)
    dao.log('Merge indexes: {0}'.format(indexes))
    dao.log('Merge data: {0}'.format(included))

    final = merge_data(excluded, included, indexes)
    dao.set_data(final)
    dao.log('Merge final count: {}'.format(len(final)))

    dao.dispose_included()
    dao.dispose_excluded()

if __name__ == '__main__' :
    fname = 'numbers.dat'
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    dao = splitdata.SplitData(fname)
    merge(dao)

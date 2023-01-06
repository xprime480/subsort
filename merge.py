import sys

def get_base(fname) :
    with open(fname + '.rem') as fh:
        return fh.readlines()

def get_data(fname) :
    with open(fname + '.out') as fh :
        data = fh.readlines()

    indexline = data[0][2:-1]
    data = data[1:]

    indexes = [int(x) for x in indexline.split(' ')]

    return data, indexes

def merge_data(base, data, indexes) :
    indexes.sort()
    stop = min(len(data), len(indexes))
    for i in range(stop) :
        where = indexes[i]
        what = data[i]
        base.insert(where, what)
    
    return base

def write_final(fname, data) :
    with open(fname, 'w') as fh :
        fh.write(''.join(data))

def merge(fname) :
    base = get_base(fname)
    data, indexes = get_data(fname)

    final = merge_data(base, data, indexes)
    write_final(fname, final)

if __name__ == '__main__' :
    fname = 'numbers.dat'
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    merge(fname)

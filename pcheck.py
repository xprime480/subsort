import sys

import splitutils

def check(fname) :
    lines = splitutils.get_data(fname)
    items = [line.split() for line in lines]
    for i in items :
        if len(i) == 2 and i[0] != i[1] :
            print(i[0], i[1])

if __name__ == '__main__' :
    fname = 'test.txt'
    if len(sys.argv) > 1 :
        fname = sys.argv[1]

    check(fname)


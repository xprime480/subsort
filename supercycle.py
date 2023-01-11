import sys

import numpy as np 
import math

import split

class SupercycleState(object) :
    def __init__(self, fname) :
        self.fname = fname
        self.state = dict()
        self.fname = fname
        self._valid = False
        self.read_state()

    def initialize(self, tiers, per_tier) :
        self.state['tiers'] = tiers
        self.state['per_tier'] = per_tier

        self.reinitialize()
        self.initialize_indexes()
        self._valid = True

    def reinitialize(self) :
        data = split.get_data(self.fname)
        count = len(data)

        count_per_tier = split.make_tier_counts(count, self.state['tiers'], self.state['per_tier'])

        self.state['count_per_tier'] = count_per_tier
        self.initialize_bases()

    def initialize_bases(self) :
        bases = []
        sum = 0
        for c in self.state['count_per_tier']:
            bases.append(sum)
            sum += c
        self.state['bases'] = bases

    def initialize_indexes(self):
        indexes = []
        sum = 0

        for c in self.state['count_per_tier']:
            ix = get_shuffled_range(sum, c)
            indexes.append(ix)
            sum += c

        self.state['indexes'] = indexes

    def read_state(self) :
        try :
            with open(self.fname + '.state') as fh :
                data = fh.read()
                d = eval(data)
                if type(d) == type(dict()) :
                    keys = ['tiers', 'per_tier', 'bases', 'indexes', 'count_per_tier']
                    for k in keys :
                        if k not in d :
                            return
                
            d.update(self.state)
            self.state = d
            self._valid = True

        except Exception as ex :
            print('Unable to open statefile', ex)

    def write_state(self) :
        if not self._valid :
            print('Not saving state because it is not valid')
            return

        with open(self.fname + '.state', 'w') as fh :
            fh.write(repr(self.state))
            fh.write('\n')

    def is_valid(self) :
        return self._valid

    def next(self) :
        indexes = self.state['indexes']
        per_tier = self.state['per_tier']

        row_index = []
        for i in range(len(indexes)):
            ix = indexes[i]
            if len(ix) < per_tier:
                ix = self.extend_index(ix, i)

            t = ix[:per_tier]
            row_index.extend(t)

            u = ix[per_tier:]
            indexes[i] = u

        self.state['indexes'] = indexes

        row_index.sort()
        return row_index

    def extend_index(self, stub, index):
        self.reinitialize()

        rest = get_shuffled_range(self.state['bases'][index], self.state['count_per_tier'][index])
        tail = []
        while len(stub) < self.state['per_tier'] and rest:
            r = rest[0]
            if r in stub:
                tail.append(r)
            else:
                stub.append(r)
            rest = rest[1:]

        stub.extend(tail)
        stub.extend(rest)

        return stub

def get_shuffled_range(start, count) :
        ix = list(range(start,start+count))
        np.random.shuffle(ix)
        return ix

if __name__ == '__main__' :
    fname = 'numbers.dat'
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    state = SupercycleState(fname)
    if not state.is_valid() :
        state.initialize(5, 2)

    for _ in range(20) : 
        sample = state.next()
        print(sample)
    state.write_state()

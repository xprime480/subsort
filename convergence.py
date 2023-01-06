import numpy as np
from operator import mul
from functools import reduce

class BinarySearcher(object) :
    def __init__(self) :
        pass

    def find_value(self) :
        lo, hi = self.init_endpoints()

        while lo < hi:
            mid = (lo + hi) // 2
            if self.check(mid):
                hi = mid
            elif lo == mid:
                lo = mid + 1
            else:
                lo = mid

        return lo

    def init_endpoints(self) :
        hi = 1
        while True:
            if self.check(hi):
                break
            hi *= 2

        lo = hi // 2

        return lo, hi

    def check(self) :
        return True

class MatrixBatchConvergence(BinarySearcher) :
    def __init__(self, size=4000, target=3600, pthresh=0.99, batch=10) :        
        self.SIZE = size
        self.TARGET = target
        self.INDEX = self.TARGET - self.SIZE - 1
        self.PTHRESH = pthresh
        self.BATCH = batch

        self.choose = self.make_pascals_row()
        self.init_transition_matrix()

        self.memo = dict()

    def init_transition_matrix(self) :
        self.m = np.zeros((self.SIZE+1, self.SIZE+1))

        for start_value in range(0,self.SIZE+1) :
            for new_count in range(self.BATCH+1) :
                if self.is_zero_entry(start_value, new_count) :
                    continue

                p = self.calculate_entry(start_value, new_count)
                self.m[start_value+new_count,start_value] = p

    def make_pascals_row(self) :
        c = []
        for x in range(self.BATCH+1) :
            c2 = [1]
            c2.extend([sum(c[index:index+2]) for index in range(len(c))])
            c = c2[:]
        return c

    def is_zero_entry(self, num_used, new_requested):
        if self.SIZE - num_used < new_requested:
            return True         # not enough new ones
        if self.BATCH - new_requested > num_used:
            return True         # not enough old ones
        
        return False

    def calculate_entry(self, start_value, new_count) :
        def ff(k, n) :
            vals = [k-i for i in range(n)]
            return reduce(mul, vals, 1)

        np = ff(self.SIZE - start_value, new_count)
        nq = ff(start_value, self.BATCH - new_count)
        nd = ff(self.SIZE, self.BATCH)
        b = self.choose[new_count]

        return (b * np * nq) / (1.0 * nd)

    def check(self, n) :
        print(n)
        if n not in self.memo :
            miter = np.linalg.matrix_power(self.m, n)
            self.memo[n] = sum(miter[:, 0][self.INDEX:])

        p = self.memo[n]
        if p >= self.PTHRESH :
            self.p_last = p
            return True
        return False

#M = MatrixBatchConvergence(size=20, target=20, batch=5)
#M = MatrixBatchConvergence()
M = MatrixBatchConvergence(size=3590, target=3590, pthresh=0.95)
value = M.find_value()
print(value, M.p_last)

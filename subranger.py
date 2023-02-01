
import numpy as np

import splitutils
import splitdata

class SubrangerState(object) :
    def __init__(self, dao, config) :
        self.dao = dao
        self.config = config

        self.spread_parm = config.float_or_default('spread', 1.0)
        self.count = config.int_or_default('item_count', 10)
        self.dao.log('Creating SubrangerState with parameters spread_parm: {0}, total_count: {1}'.format(self.spread_parm, self.count))

        self.data = self.dao.get_data()
        self.datalen = len(self.data)
        self.dao.log('Data length = {0}'.format(self.datalen))

        if self.spread_parm > 1.0 :
            self.spread = max(min(self.datalen, int(self.spread_parm)), self.count)
        else :
            self.spread = max(int(self.datalen * self.spread_parm), self.count)

        self.dao.log('Adjusted parameters: spread: {0}'.format(self.spread))

    def next(self) :
        if self.datalen <= self.count:
            return list(range(len))

        maxbase = self.datalen - self.spread
        base = 0
        if maxbase > base:
            base = np.random.randint(0, maxbase+1)

        indexes = splitutils.get_subset_from_range(base, base+self.spread, self.count)
        indexes.sort()
        return indexes

    def finalize(self) :
        pass

def get_dao(config):
    return splitdata.get_dao(config)

def get_indexer(config, dao):
    return SubrangerState(dao, config)

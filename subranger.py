
import numpy as np

import splitutils
import splitdata

class SubrangerState(object) :
    def __init__(self, dao, config) :
        self.dao = dao
        self.config = config

        self.spread = config.int_or_default('spread', 1000000)
        self.count = config.int_or_default('item_count', 10)
        self.dao.log('Creating SuperCycleState with parameters spread: {0}, total_count: {1}'.format(self.spread, self.count))

        self.data = self.dao.get_data()
        self.datalen = len(self.data)
        self.dao.log('Data length = {0}'.format(self.datalen))

        self.spread = max(min(self.datalen, self.spread), self.count)

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

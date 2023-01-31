import numpy as np

import splitdata

class StriderState(object) :
    def __init__(self, dao, config) :
        self.dao = dao
        self.config = config

        self.count = config.int_or_default('item_count', 10)
        self.max_width = config.int_or_default('max_width', 1000000)
        self.dao.log('Creating StriderState with parameters total_count: {0}, max_width: {1}'.format(self.count, self.max_width))

        data = self.dao.get_data()
        datalen = len(data)
        self.dao.log('Data length = {0}'.format(datalen))

        self.width = min(datalen // self.count, self.max_width)
        self.basemax = datalen - 1 - (self.count - 1) * self.width

    def next(self) :
        base = np.random.randint(0, self.basemax+1)
        indexes = [base + i * self.width for i in range(self.count)]
        return indexes

    def finalize(self) :
        pass

def get_dao(config):
    return splitdata.get_dao(config)

def get_indexer(config, dao):
    return StriderState(dao, config)

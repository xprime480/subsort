import sys
import importlib

import splitutils
import splitconfig

def get_data(dao, indexer) :
    indexes = indexer.next()
    data = dao.get_data()
    new = dao.get_new()

    if not new or len(indexes) == 0 :
        return data, indexes

    indexes.append(len(data))
    data.append(new[0])
    dao.set_new(new[1:])

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

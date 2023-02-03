import sys
import importlib

import splitutils
import splitconfig

def split(dao, indexer):
    indexes = indexer.next()

    dao.log('Split indexes: {0}'.format(indexes))
    included, excluded = splitutils.partition_by_index(dao.get_data(), indexes)
    dao.log('Split data: {0}'.format(included))

    dao.set_included(included, indexes)
    dao.set_excluded(excluded)
    indexer.finalize()

if __name__ == '__main__':
    fname = 'numbers.config'
    if len(sys.argv) > 1 :
        fname = sys.argv[1]

    config = splitconfig.SplitConfig(fname)
    if not config.is_ready() :
        print('Error reading config')
        sys.exit(1)

    package = config.get_or_default('package', '')
    if package :
        try :
            lib = importlib.import_module(package)
        except Exception as ex :
            print('Error importing pakage {0}: {1}'.format(package, ex))
            
        dao = lib.get_dao(config)
        indexer = lib.get_indexer(config, dao)
        split(dao, indexer)

    else :
        print('No valid package was specified, cannot split')


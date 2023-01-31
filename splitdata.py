import os
import datetime

import splitutils

class SplitData(object) :
    def __init__(self, fname) :
        self.fname = fname
        self.data = None
        self.included = None
        self.excluded = None
        self.state = None

    def get_data(self) :
        if not self.data :
            self.data = splitutils.get_data(self.fname)
        return self.data

    def set_data(self, data) :
        self.data = data
        def writer(fh):
            self.write_joined_lines(fh, self.data)
        splitutils.write_or_unlink(self.data, self.fname, writer)

    def get_state(self) :
        if not self.state :
            fname = self.get_state_fname()
            self.state = splitutils.get_data(fname)
        return self.state

    def set_state(self, newstate) :
        self.state = newstate
        fname = self.get_state_fname()
        def writer(fh) :
            self.write_joined_lines(fh, self.state)

        splitutils.write_or_unlink(self.state, fname, writer)

    def get_state_fname(self) :
        return self.fname + '.state'

    def get_included(self) :
        if not self.included :
            fname = self.get_included_fname()
            self.included = splitutils.get_data(fname)
        return self.included

    def set_included(self, included, indexes):
        self.included = included
        fname = self.get_included_fname()
        def writer(fh):
            self.write_header_line(fh, indexes)
            self.write_joined_lines(fh, self.included)

        splitutils.write_or_unlink(self.included, fname, writer)

    def dispose_included(self) :
        self.dispose(self.get_included_fname())

    def get_included_fname(self) :
        return self.fname + '.out'

    def get_excluded(self) :
        if not self.excluded:
            fname = self.get_excluded_fname()
            self.excluded = splitutils.get_data(fname)
        return self.excluded

    def set_excluded(self, excluded):
        self.excluded = excluded
        fname = self.get_excluded_fname()
        def writer(fh) :
            fh.write('\n'.join(excluded))
            fh.write('\n')

        splitutils.write_or_unlink(self.excluded, fname, writer)

    def dispose_excluded(self):
        self.dispose(self.get_excluded_fname())

    def get_excluded_fname(self):
        return self.fname + '.rem'

    def write_header_line(self, fh, indexes) :
        fh.write('# ')
        fh.write(' '.join([str(i) for i in indexes]))
        fh.write('\n')

    def write_joined_lines(self, fh, lines) :
        fh.write('\n'.join(lines))
        fh.write('\n')

    def dispose(self, fname) :
        os.unlink(fname)

    def log(self, msg) :
        fname = self.fname + '.log'
        now = datetime.datetime.now()
        with open(fname, 'a+') as fh :
            if type(msg) == type([]) :
                for m in msg :
                    fh.write('[{0}] {1}\n'.format(now, m))
            else :
                fh.write('[{0}] {1}\n'.format(now, msg))

def get_dao(config) :
    fname = 'numbers.dat'

    if config:
        root = config.get_or_default('file_root', '')
        if root:
            fname = root
        path = config.get_or_default('file_path', '.')
        if path:
            fname = os.path.join(path, fname)

    return SplitData(fname)

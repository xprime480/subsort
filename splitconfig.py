import sys
import os

INITIALIZING = 0
READY = 1
ERRORED = -1

class SplitConfig(object) :
    def __init__(self, fname) :

        self.state = INITIALIZING

        self.config = dict()
        self.config['config_file'] = fname

        try :
            with open(fname) as fh :
                lines = fh.readlines()
        except Exception as ex:
            self.config['error_message'] = ex
            self.state = ERRORED
            return

        pairs = [x.split('=') for x in lines]
        for p in pairs :
            if len(p) == 1 :
                key = p[0].strip()
                self.config[key] = True
            elif len(p) == 2 :
                key = p[0].strip()
                val = p[1].strip()
                self.config[key] = val
            else : 
                print("Questionable data", p)

        if 'file_path' not in self.config :
            self.config['file_path'] = os.path.dirname(os.path.realpath(fname))

        self.state = READY

    def get_or_default(self, key, default, convert = lambda x: x):
        if not key in self.config:
            return default

        v = self.config[key]
        try : 
            return convert(v)
        except :
            return default

    def int_or_default(self, key, default):
        return self.get_or_default(key, default, lambda x: int(x))

    def float_or_default(self, key, default) :
        return self.get_or_default(key, default, lambda x: float(x))
    
    def list_of_int_or_default(self, key, default) :
        value = self.get_or_default(key, '')
        if not value :
            return default
        
        items = value.split(',')
        return [int(i) for i in items]

    def is_ready(self) :
        return self.state == READY

if __name__ == '__main__' :
    fname = 'numbers.config'

    if len(sys.argv) > 1 :
        fname = sys.argv[1]

    config = SplitConfig(fname) 
    print(config.config)
    print(config.int_or_default('first_tier_min', 1))
    print(config.int_or_default('booble', 2))
    print(config.float_or_default('tier_ratio', 3.1415))
    print(config.float_or_default('snooble', 7.71113))
    print(config.get_or_default('package', 'nothing'))
    print(config.get_or_default('a-key', 'a-default-value'))

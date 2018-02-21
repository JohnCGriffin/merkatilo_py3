
__all__ = [ 'lo' ]

import os
import threading
import merkatilo.core as core
import merkatilo.obs_series as obs_series

def __normalize_id(name):
    name = name.upper()
    if name.find("::") < 0:
        name = '{}::CLOSE'.format(name)
    return name

def __default_loader(id):
    normalized_id = __normalize_id(id)
    ticker,subject = normalized_id.split('::')
    fname = '{}/TIME_SERIES/{}/{}'.format(os.getenv('HOME'), ticker, subject)
    entries = []
    with open(fname) as f:
        for line in f:
            try:
                pair = line.split()
                entries.append((core.to_jdate(pair[0]),float(pair[1])))
            except:
                pass
    return obs_series.obs_to_series(entries, name=normalized_id)

__local = threading.local()
__local.loader = __default_loader

# Return active loader with optional setting
def loader(f=None):
    result = __local.loader
    if f:
        __local.loader = f
    return result

def lo(id):
    
    '''The :code:`lo(ID)` command is a sample mechanism for 
    importing time series.  You will likely need to create your 
    own implementation of a loader and set it with
    merkatilo.load.loader(your_function)'''

    return __local.loader(id)



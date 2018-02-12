
__all__ = [ 'lo' ]

import os
import merkatilo.core as core
import merkatilo.obs_series as obs_series

def lo(name):
    
    '''The lo(ID) command is a sample mechanism for importing time series.
    You will likely need to create your own implementation.'''
    
    fname = '{}/TIME_SERIES/{}/CLOSE'.format(os.getenv('HOME'),name)
    entries = []
    with open(fname) as f:
        for line in f:
            try:
                pair = line.split()
                entries.append((core.to_jdate(pair[0]),float(pair[1])))
            except:
                pass
    return obs_series.obs_to_series(entries, name=name)



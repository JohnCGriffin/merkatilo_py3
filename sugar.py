
__all__ = [ 'lo_set_dates' ]

import load, core

def lo_set_dates(item):
    s = load.lo(item)
    core.set_dates(s)
    return s


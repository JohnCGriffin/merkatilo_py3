
__all__ = [ 'lo_set_dates' ]

import load, core

def lo_set_dates(item):
    
    '''load a series, set the current_dates parameter for side-effect, 
    and finally return the series'''
    
    s = load.lo(item)
    core.set_dates(s)
    return s


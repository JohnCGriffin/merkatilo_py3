
__all__ = [ 'lo_set_dates' ]

from merkatilo.load import lo
import merkatilo.core as core

def lo_set_dates(item):
    
    '''load a series, set the current_dates parameter for side-effect, 
    and finally return the series'''
    
    s = lo(item)
    core.set_dates(s)
    return s



__all__ = [ 'series_filter' ]

import merkatilo.core as core
from merkatilo.private.abbreviate import abbreviate

# e.g. series_filter(lambda val:(180 < val < 190), IBM)

def series_filter(predicate, s):
    
    '''For each observation in series, check the predicate against
    the value. Passing observations dictate existence in the output series.'''
    
    base_f = s.f
    def f(dt):
        val = base_f(dt)
        return val if (core.is_valid_num(val) and predicate(val)) else None
    name='filter({},{})'.format(abbreviate(predicate),abbreviate(s))
    return core.series(f, name=name)

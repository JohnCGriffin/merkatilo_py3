
__all__ = [ 'fudge' ]

import merkatilo.core as core
from merkatilo.private.abbreviate import abbreviate

def fudge(s, days=6):
    
    '''fudge decorates a series such that the query by date 
    will continue looking backward until it finds a value,
    up to the number of days specified, defaulting to 
    six days.  Six days permits weekly and daily market 
    data to align dates with ends of 
    months, quarters and years.'''
    
    sf = s.f
    def f(dt):
        for i in range(days+1):
            val = sf(dt-i)
            if core.is_valid_num(val):
                return val
        return None
    name = ("fudge({})".format(abbreviate(s)) if days==6
            else "fudge({},{})".format(abbreviate(s),days))
    return core.series(f, name=name)


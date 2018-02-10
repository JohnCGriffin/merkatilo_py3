
__all__ = [ 'series_filter' ]

import core
from private.abbreviate import abbreviate

# e.g. series_filter(lambda val:(180 < val < 190), IBM)

def series_filter(proc, s):
    base_f = s.f
    def f(dt):
        val = base_f(dt)
        return val if (core.is_valid_num(val) and proc(val)) else None
    name='filter({},{})'.format(abbreviate(proc),abbreviate(s))
    return core.series(f, name=name)

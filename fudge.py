
__all__ = [ 'fudge' ]

import core
from private.abbreviate import abbreviate

def fudge(s, days=6):
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


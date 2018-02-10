
__all__ = [ 'series_or', 'series_and' ]

import core
from private.abbreviate import abbreviate


def series_and(a,b):
    af = a.f
    bf = b.f
    def f(dt):
        a_val = af(dt)
        if core.is_valid_num(a_val):
            b_val = bf(dt)
            if core.is_valid_num(b_val):
                return b_val
        return False
    name='and({},{})'.format(abbreviate(a),abbreviate(b))
    return core.series(f, name=name)

def series_or(a,b):
    af = a.f
    bf = b.f
    def f(dt):
        result = af(dt)
        if is_valid_num(result):
            return result
        return bf(dt)
    name='or({},{})'.format(abbreviate(a),abbreviate(b))
    return core.series(f,name=name)


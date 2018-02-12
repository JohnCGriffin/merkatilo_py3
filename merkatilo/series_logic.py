
__all__ = [ 'series_or', 'series_and' ]

import merkatilo.core as core
from merkatilo.private.abbreviate import abbreviate


def series_and(a,b):

    '''Given two series, return a series such that the output value is the value
    of the second input series if both input series have values at a date.'''
    
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

    '''Given two series, return a series such that the output value is the value
    of the first input series if has a value, otherwise the value from the second
    input series.'''
    
    af = a.f
    bf = b.f
    def f(dt):
        result = af(dt)
        if is_valid_num(result):
            return result
        return bf(dt)
    name='or({},{})'.format(abbreviate(a),abbreviate(b))
    return core.series(f,name=name)


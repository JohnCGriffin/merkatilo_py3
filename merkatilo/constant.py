
__all__ = [ 'constant' ]

import merkatilo.core as core

def constant(N):
    '''Return a series that always responds with the same number N.'''
    def f(dt_ignored):
        return N
    return core.series(lambda ignored:N,
                       name="constant({})".format(N),
                       require_normalization_wrapper=False)

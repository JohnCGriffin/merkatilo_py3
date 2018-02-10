
__all__ = [ 'constant' ]

import core

def constant(N):
    def f(dt_ignored):
        return N
    return core.series(lambda ignored:N,
                       name="constant({})".format(N),
                       require_normalization_wrapper=False)

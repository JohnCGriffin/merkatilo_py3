
__all__ = [ 'constant' ]

import merkatilo.core as core

def constant(N):
    def f(dt_ignored):
        return N
    return core.series(lambda ignored:N,
                       name="constant({})".format(N),
                       require_normalization_wrapper=False)

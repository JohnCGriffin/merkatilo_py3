
__all__ = [ 'prepend' ]

import merkatilo.core as core
from merkatilo.private import series_dates_values
from first_last_ob import first_ob
from series_binop import add

def prepend (s, *, surrogate=None, dates=None):

    dates = (dates or core.current_dates())
    if surrogate is None:
        raise Exception("surrogate required")
    ob = first_ob(add(s,surrogate), dates=dates)
    if ob is None:
        raise Exception("no observation")
    
    base_f = s.f
    surr_f = surrogate.f
    common_date = ob[0]
    ratio = s.f(ob[0]) / surr_f(ob[0])

    dv = dates.vec
    fd = dates.first_date()
    ld = dates.last_date()
    outv = [ None for dt in range(fd,ld+1) ]

    for (ndx, dt) in enumerate(dv):
        val = base_f(dt)
        if not core.is_valid_num(val) and dt < common_date:
            val = surr_f(dt) * ratio
        if core.is_valid_num(val):
            outv[dt - fd] = val

    return core.vector_series(outv, fd, name="prepend(...)")




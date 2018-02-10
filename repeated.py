
__all__ = [ 'repeated' ]

import core

def repeated(s, repeat_last=False, dates=None):

    '''Fill missing values in a series with preceding ones, optionally
    continuing the last valid observation.'''

    dates = dates or core.current_dates()
    vals = list(map(s.f,dates))

    fd = dates.first_date()
    ld = dates.last_date()

    prev = vals[0]
    last_valid_date = fd
    for ndx,val in enumerate(vals):
        if ndx and not core.is_valid_num(val):
            vals[ndx] = prev
        else:
            last_valid_date = dates.vec[ndx]
        prev = vals[ndx]

    fd = dates.first_date()
    ld = dates.last_date()

    outv = [ None for dt in range(fd,ld+1) ]

    for (dt,val) in zip(dates,vals):
        if (not repeat_last) and (dt > last_valid_date):
            break
        if core.is_valid_num(val):
            outv[dt - fd] = val

    return core.vector_series(outv, fd)
    

    

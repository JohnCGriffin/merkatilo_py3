
__all__ = [ 'unrepeated' ]

import merkatilo.core as core

def unrepeated(s, dates=None):

    '''Copy the input series, suppressing repeated values.'''

    dates = dates or core.current_dates()
    vals = list(map(s.f,dates))

    prev = vals[0]
    for ndx,val in enumerate(vals):
        if ndx and val == prev:
            vals[ndx] = None
        prev = val

    fd = dates.first_date()
    ld = dates.last_date()

    outv = [ None for dt in range(fd,ld+1) ]

    for (dt,val) in zip(dates,vals):
        if core.is_valid_num(val):
            outv[dt - fd] = val

    return core.vector_series(outv, fd)
    

    

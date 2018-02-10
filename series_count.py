
__all__ = [ 'series_count' ]

import core

def series_count(s, dates=None):
    '''Return the number of observations.  The typical
    use of this is in unit testing.'''
    dates = dates or core.current_dates()
    sf = s.f
    return sum((1 for dt in dates if sf(dt)))


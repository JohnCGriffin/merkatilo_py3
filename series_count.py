
__all__ = [ 'series_count' ]

import core

def series_count(s, dates=None):
    dates = dates or core.current_dates()
    sf = s.f
    return sum((1 for dt in dates if sf(dt)))


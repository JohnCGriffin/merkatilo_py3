
__all__ = [ 'series_dates_values' ]

def series_dates_values(s, dts):
    f = s.f
    return [ f(dt) for dt in dts.vec ]

    

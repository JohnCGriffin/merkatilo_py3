
__all__ = [ 'obs_to_series', 'series_to_obs' ]

import core

def obs_to_series(obs, name=None):
    valids = [ (core.to_jdate(ob[0]),ob[1]) for ob in obs if ob ]
    valids.sort()
    if not len(valids):
        return core.series(lambda dt: None, name)
    fd = valids[0][0]
    ld = valids[-1][0]
    vec:List[Optional[float]] = [ None for x in range(fd,ld+1) ]
    for (dt,val) in valids:
        vec[dt-fd] = val
    return core.vector_series(vec, fd, name=name)

def series_to_obs(dates, s):
    f = s.f
    return [ (dt,f(dt)) for dt in dates if core.is_valid_num(f(dt)) ]



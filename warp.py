
__all__ = [ 'warp' ]

import core
from private import series_dates_values

def warp (s, N:int, dates=None):

    dates = (dates or core.current_dates())
    dv = dates.vec
    sf = s.f
    fd = dates.first_date()
    ld = dates.last_date()
    outv = [ None for dt in range(fd,ld+1) ]

    for (ndx, dt) in enumerate(dv):
        val = sf(dt)
        if val:
            new_ndx = ndx+N
            if 0 <= new_ndx < len(dv):
                new_dt = dv[new_ndx]
                outv[new_dt - fd] = val

    return core.vector_series(outv, fd, name="warp({})".format(N))



#==========================================

import unittest
from series_count import series_count
from load import lo

class warp_testing(unittest.TestCase):

    def test_two_way(self):
        IBM = lo('IBM')
        core.current_dates(core.dates(IBM))
        self.assertEqual(series_count(warp(IBM,20)),
                         series_count(IBM)-20)

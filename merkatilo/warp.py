
__all__ = [ 'warp' ]

import merkatilo.core as core
from merkatilo.private import series_dates_values

def warp (s, N, dates=None):

    '''N-period shift of values within dateset.  Negative periods shift data
    backward in time.  Often a signal series if warped with N=1 to measure 
    performance of a trading scheme if trading happens the next market day.'''

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

from merkatilo.common_testing_base import CommonTestingBase
from merkatilo.series_count import series_count

class warp_testing(CommonTestingBase):

    def test_two_way(self):
        self.assertEqual(series_count(warp(self.TEST_SERIES,20)),
                         series_count(self.TEST_SERIES)-20)

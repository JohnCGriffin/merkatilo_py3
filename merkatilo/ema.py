
__all__ = [ 'ema' ]

import merkatilo.core as core
from merkatilo.private.abbreviate import abbreviate


def ema(s, N, dates=None):
    
    '''An ema smoothes a series such that the current value is weighted by some fraction 
    in (0..1) added to the previous value weighted by (1 - fraction).  The 
    fraction is calculated as (2/(N+1)).'''
    
    dates = dates or core.current_dates()
    fd,ld = s.first_date(),s.last_date()
    outv = [ None for dt in range(fd,ld+1) ]
    fraction = 2/(N+1)
    remainder = 1 - fraction
    prev = None
    f = s.f
    for dt in dates:
        val = f(dt)
        newVal = ((fraction * val + remainder * prev)
                  if (core.is_valid_num(prev) and core.is_valid_num(val))
                  else val)
        outv[dt - fd] = newVal
        prev = newVal
    return core.vector_series(outv, fd, name="EMA({},{})".format(abbreviate(s),N))



#=================================

from merkatilo.common_testing_base import CommonTestingBase, obs_to_series
from merkatilo.private.test_support import EMA_3_OBS


class EMATest(CommonTestingBase):

    def test_ema_3(self):
        EMA_3_SERIES = obs_to_series(EMA_3_OBS)
        f1 = EMA_3_SERIES.f
        f2 = ema(self.TEST_SERIES,3).f
        for dt in core.current_dates():
            self.assertEqual(f1(dt),f2(dt))


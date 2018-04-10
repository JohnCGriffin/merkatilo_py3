
__all__ = [ 'ema', 'fractional' ]

import merkatilo.core as core
from merkatilo.private.abbreviate import abbreviate


def fractional(s, fraction, dates=None):
    
    '''A fractional smoothes a series such that the current value is weighted by some fraction 
    in (0..1) added to the previous value weighted by (1 - fraction).'''
    
    dates = dates or core.current_dates()
    fd,ld = s.first_date(),s.last_date()
    outv = [ None for dt in range(fd,ld+1) ]
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
    return core.vector_series(outv, fd, name="fractional({},{})".format(abbreviate(s),fraction))


def ema(s, N, dates=None):
    
    '''An ema smoothes a series such that the current value is weighted by some fraction 
    in (0..1) added to the previous value weighted by (1 - fraction).  The 
    fraction is calculated as (2/(N+1)).'''

    return fractional(s, 2/(N+1), dates=dates)




#=================================

from merkatilo.common_testing_base import CommonTestingBase, obs_to_series
from merkatilo.private.test_support import EMA_3_OBS


class EMATest(CommonTestingBase):

    def test_ema_3(self):
        EMA_3_SERIES = obs_to_series(EMA_3_OBS)
        self.verify_two_series(ema(self.TEST_SERIES,3), EMA_3_SERIES)

    def test_ema_fractional(self):
        f = fractional(self.TEST_SERIES,.5)
        self.verify_two_series(ema(self.TEST_SERIES,3), f)
        


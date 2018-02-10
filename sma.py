
__all__ = [ 'sma' ]

import core
from private.series_dates_values import series_dates_values

def sma(s, N, dates=None):

    '''Create running N-period arithmetic average of input series.'''
    
    dates = dates or core.current_dates()
    vals = series_dates_values(s,dates)
    fd = dates.first_date()
    ld = dates.last_date()
    outv = [ None for dt in range(fd,ld+1) ]

    total = 0
    consecutive = 0
    
    for ndx,dt in enumerate(dates):
        val = vals[ndx]
        if core.is_valid_num(val):
            total += val
            consecutive += 1
        if consecutive > N:
            total -= vals[ndx-N]
        if consecutive >= N:
            outv[dt - fd] = (total / N)
        
    return core.vector_series(outv, fd, name = "SMA({})".format(N))
    
#=================================

from common_testing_base import CommonTestingBase, obs_to_series
from private.test_support import SMA_3_OBS

class SMATest(CommonTestingBase):

    def test_sma_3(self):
        SMA_3_SERIES = obs_to_series(SMA_3_OBS)
        core.current_dates(core.dates(self.TEST_SERIES))
        f1 = SMA_3_SERIES.f
        f2 = sma(self.TEST_SERIES,3).f
        for dt in core.current_dates():
            f1_val = f1(dt)
            f2_val = f2(dt)
            self.assertEqual(f1_val, f2_val)

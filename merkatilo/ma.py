
__all__ = [ 'sma', 'ma' ]

import merkatilo.core as core
from merkatilo.private.series_dates_values import series_dates_values

def ma(s, N, dates=None):

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
        else:
            consecutive = 0
            total = 0
        if consecutive > N:
            total -= vals[ndx-N]
        if consecutive >= N:
            outv[dt - fd] = (total / N)
        
    return core.vector_series(outv, fd, name = "SMA({})".format(N))

# temporary compatibility
sma = ma
    
#=================================

from merkatilo.common_testing_base import CommonTestingBase, obs_to_series
from merkatilo.private.test_support import MA_3_OBS

class SMATest(CommonTestingBase):

    def test_ma_3(self):
        MA_3_SERIES = obs_to_series(MA_3_OBS)
        self.verify_two_series(ma(self.TEST_SERIES,3), MA_3_SERIES)

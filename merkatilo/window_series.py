
__all__ = [ 'window_series' ]

import merkatilo.core as core
from merkatilo.private import series_dates_values

def window_series (s, N, proc, dates=None, missing_data_permitted=False):

    dates = (dates or core.current_dates())
    dv = dates.vec
    sf = s.f
    fd = dates.first_date()
    ld = dates.last_date()
    vv = [(n if core.is_valid_num(n) else None) for n in (sf(dt) for dt in dv)]
    outv = [ None for dt in range(fd,ld+1) ]

    count = 0
    for (ndx, dt) in enumerate(dv):
        val = sf(dt)
        count = (count+1 if (missing_data_permitted or core.is_valid_num(val)) else 0)
        if count >= N:
            stop = ndx+1
            start = stop-N
            result = proc(vv[start:stop])
            if core.is_valid_num(result):
                outv[dt - fd] = result

    return core.vector_series(outv, fd, name="window_series({})".format(N))



#==========================================

from merkatilo.common_testing_base import CommonTestingBase
from merkatilo.sma import sma

class WindowSeriesTest(CommonTestingBase):

    def test_alternate_sma(self):
        for period in range(10,50,5):
            SMA_SERIES = sma(self.TEST_SERIES,period)
            CHECK_SERIES = window_series(self.TEST_SERIES, period, lambda xs:(sum(xs)/len(xs)))
            self.verify_two_series(SMA_SERIES,CHECK_SERIES)

    def test_alternate_sma_calendar_dates(self):
        with core.date_scope(core.date_range("2013-1-1","2013-12-31")):
            SMA_SERIES = sma(self.TEST_SERIES,3)
            CHECK_SERIES = window_series(self.TEST_SERIES, 3, lambda xs:(sum(xs)/len(xs)))
            self.verify_two_series(SMA_SERIES,CHECK_SERIES)



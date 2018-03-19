
__all__ = [ 'calibrate' ]

import merkatilo.core as core
from merkatilo.private.abbreviate import abbreviate


def calibrate(s, init=100, date=None):

    '''To calibrate a series is to make it value-compatible with another.
    For example, a spider graph picks a point at which multiple time
    series are the same value.  The default date is the beginning of the
    dateset and the default value of the series there is 100, making any
    value in the series equivalent to the percentage of the beginning.'''

    date = core.to_date(date) or core.first_date()
    f = s.f
    val = f(date)

    if not core.is_valid_num(val):
        raise Exception("no observation at {}".format(date))

    ratio = init / val

    def fetcher(dt):
        val = f(dt)
        if core.is_valid_num(val):
            val = val * ratio
        return val

    return core.series(fetcher, "calibrate({})".format(abbreviate(s)))



#=================================

from merkatilo.common_testing_base import CommonTestingBase
from merkatilo.series_binop import mul

class CalibrateTesting(CommonTestingBase):

    def test_100(self):
        cal = calibrate(self.TEST_SERIES)
        ratio = 100 / self.TEST_SERIES.f(core.first_date())
        self.verify_two_series(cal, mul(self.TEST_SERIES, ratio))

    def test_22(self):
        cal = calibrate(self.TEST_SERIES, init=22)
        ratio = 22 / self.TEST_SERIES.f(core.first_date())
        self.verify_two_series(cal, mul(self.TEST_SERIES, ratio))

    def test_date(self):
        cal = calibrate(self.TEST_SERIES, date='2014-12-31')
        ratio = 100 / self.TEST_SERIES.f(core.to_date('2014-12-31'))
        self.verify_two_series(cal, mul(self.TEST_SERIES, ratio))



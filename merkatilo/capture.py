
__all__ = [ 'up_capture', 'down_capture' ]

import merkatilo.core as core
from merkatilo.private import series_dates_values
from merkatilo.momentum import mo

def capture (s, benchmark, period, dates, predicate):

    if not benchmark:
        raise Exception("benchmark series must be specified")
    if not period:
        raise Exception("expected period > 0")

    dates = (dates or core.current_dates())

    sf = mo(s,period).f
    bf = mo(benchmark,period).f

    B_total = 0
    S_total = 0

    for dt in dates.vec:
        B_val = bf(dt)
        if core.is_valid_num(B_val) and predicate(B_val):
            S_val = sf(dt)
            if core.is_valid_num(S_val):
                B_total = B_total + B_val
                S_total = S_total + S_val

    return (S_total / B_total) if B_total else None

def up_capture(s, *, benchmark=None, period=None, dates=None):
    return capture(s,benchmark,period,dates,lambda a : a > 0)

def down_capture(s, *, benchmark=None, period=None, dates=None):
    return capture(s,benchmark,period,dates,lambda a : a < 0)


#==========================================

from merkatilo.common_testing_base import CommonTestingBase,approx
from merkatilo.warp import warp


class capture_testing(CommonTestingBase):

    def test_down_capture(self):
        S = self.TEST_SERIES
        self.assertEqual(
            approx(down_capture(S, benchmark=warp(S,10), period=63)),
            approx(0.5898654044835749))


__all__ = [ 'equity_line' ]

import merkatilo.core as core
from merkatilo.constant import constant
from merkatilo.private.series_dates_values import series_dates_values
from merkatilo.first_last_ob import first_ob

def equity_line(s, signals, initial_value=100, alternate_investment=None, dates=None):

    '''The point of most signal generation is to go in and out of invested position
    on some series, optionally buying an alternate investment such as short-duration debt.
    The equity_line series represents the value of the investment after treating signals
    as entrance and exit points during the dateset indicated.'''

    dates = dates or core.current_dates()
    dv = dates.vec
    fd = dates.first_date()
    ld = dates.last_date()
    alternate_investment = alternate_investment or constant(1)

    alt_vals = series_dates_values(alternate_investment,dates)
    inv_vals = series_dates_values(s,dates)
    sig_vals = series_dates_values(signals,dates)

    outv = [ None for dt in range(fd,ld+1) ]

    product = 1.0
    buy = True
    prev_inv = prev_alt = None
    first_sig_ob = first_ob(signals, dates=dates)
    if not first_sig_ob:
        raise Exception("signal series is empty")

    for (dt,alt,inv,sig) in zip(dv,alt_vals,inv_vals,sig_vals):
        if sig or (core.is_valid_num(alt) and core.is_valid_num(inv)):
            change = None
            if not core.is_valid_num(inv):
                raise Exception("missing investment observation at {}".format(
                    core.jdate_to_text(dt)))
            if not core.is_valid_num(alt):
                raise Exception("missing alternate_investment observation at {}".format(
                    core.jdate_to_text(dt)))
            if buy:
                if prev_inv:
                    change = inv/prev_inv
                else:
                    change = 1.0
            else:
                if prev_alt:
                    change = alt/prev_alt
                else:
                    change = 1.0

            # prior to having signal, nothing was invested
            if dt <= first_sig_ob[0]:
                change = 1.0

            new_buy = (sig > 0) if sig else buy
            new_product = product * change
            
            outv[dt - fd] = new_product * initial_value

            product = new_product
            buy = new_buy
            prev_inv = inv
            prev_alt = alt

    return core.vector_series(outv, fd)


#============================================

from merkatilo.common_testing_base import *
from merkatilo.cross import cross
from merkatilo.ema import ema
from merkatilo.private.test_support import EQUITYLINE_EMA_10_OBS

class EquitylineTests(CommonTestingBase):

    def testCrossEMA10(self):
        crossed = equity_line(self.TEST_SERIES,
                             cross(slower=ema(self.TEST_SERIES,10),
                                   faster=self.TEST_SERIES))
        EQUITYLINE_EMA_10_SERIES = obs_to_series(EQUITYLINE_EMA_10_OBS)
        f1 = crossed.f
        f2 = EQUITYLINE_EMA_10_SERIES.f
        for dt in core.current_dates():
            self.assertEqual(f1(dt),f2(dt))

        

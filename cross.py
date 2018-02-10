
__all__ = [ 'cross' ]

import core, obs_series
from private.series_dates_values import series_dates_values


def cross(*,slower=None, faster=None, upfactor=1.0, downfactor=1.0, dates=None):
    '''cross generates a signal series, i.e. series of [1,-1,None], set to 1
    where the faster series moves above the slower series and -1 where it moves
    below. Changing the upfactor from its default 1.0 changes the border for 
    crossing.  For instance, upfactor=1.02 means that the faster series must 
    exceed the lower series by 2% before generating the buy value of 1.  Likewise,
    setting downfactor to .98 would require passing 2% below the faster series
    to generate a sell signal of -1.  As usual, dates can be supplied, but default
    to the current_dates() value.'''

    if (not slower) or (not faster):
        raise Exception('slower,faster are required keyword arguments')

    dates = dates or core.current_dates()
    sv = series_dates_values(slower, dates)
    fv = series_dates_values(faster, dates)

    obs = []
    prev_sig = None
    
    for ndx,dt in enumerate(dates):
        s_val = sv[ndx]
        f_val = fv[ndx]

        if not (core.is_valid_num(s_val) and core.is_valid_num(f_val)):
            continue

        if f_val > s_val * upfactor:
            sig = 1
        elif f_val < s_val * downfactor:
            sig = -1
        else:
            sig = None

        if sig and (sig != prev_sig):
            obs.append((dt,sig))
            prev_sig = sig

    return obs_series.obs_to_series(obs)

        
          
        
        
#======================================

from common_testing_base import CommonTestingBase, obs_to_series
from ema import ema
from private.test_support import CROSS_EMA_30_OBS

class CrossTests(Comm

    def test_cross(self):
        CROSS_EMA_30_SERIES = obs_to_series(CROSS_EMA_30_OBS)
        f1 = CROSS_EMA_30_SERIES.f
        f2 = cross(slower=ema(self.TEST_SERIES,30), faster=self.TEST_SERIES).f
        for dt in core.current_dates():
            self.assertEqual(f1(dt),f2(dt))

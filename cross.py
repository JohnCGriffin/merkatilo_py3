
__all__ = [ 'cross' ]

import core, obs_series
from private.series_dates_values import series_dates_values


def cross(*,slower=None, faster=None, upfactor=1.0, downfactor=1.0, dates=None):

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

import unittest
from obs_series import obs_to_series
from ema import ema

from private.test_support import TEST_SERIES_OBS, CROSS_EMA_30_OBS

class CrossTests(unittest.TestCase):

    def test_cross(self):
        TEST_SERIES = obs_to_series(TEST_SERIES_OBS)
        CROSS_EMA_30_SERIES = obs_to_series(CROSS_EMA_30_OBS)
        core.current_dates(core.dates(TEST_SERIES))
        f1 = CROSS_EMA_30_SERIES.f
        f2 = cross(slower=ema(TEST_SERIES,30), faster=TEST_SERIES).f
        for dt in core.current_dates():
            self.assertEqual(f1(dt),f2(dt))

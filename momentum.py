
__all__ = [ 'mo', 'mo_days' ]

import core, fudge
from private.abbreviate import abbreviate

def ratio(early, late):
    return (late/early - 1.0) if (core.is_valid_num(late) and core.is_valid_num(early)) else None

def mo(s, N, dates=None):
    '''return the N-period ratio of new/old values.'''
    
    if N < 1:
        raise Exception('requires period > 0')

    dates = dates or core.current_dates()
    sf = s.f
    dv = dates.vec
    shifted_dv = dv[min(N,len(dv)):]
    outv = [ None for dt in range(dv[0],dv[-1]+1) ]
    fd = dv[0]

    for (early,late) in zip(dv,shifted_dv):
        e_val = sf(early)
        l_val = sf(late)
        r = ratio(e_val, l_val)
        if core.is_valid_num(r):
            outv[late - fd] = r

    name = "mo({},{})".format(abbreviate(s),N)
    return core.vector_series(outv, fd, name=name)


def mo_days(s, days, dates=None):
    
    '''Similar to mo(s,N), mo_days(s,days) calculate the new/old ratios along
    the specified dates but the old is based upon calendar days rather than 
    periods.'''
    
    sf = s.f
    sf_old = (fudge.fudge(s)).f

    if days < 1:
        raise Exception('expected positive days')

    dates = dates or core.current_dates()
    dv = dates.vec
    fd = dv[0]
    outv = [ None for dt in range(dv[0],dv[-1]+1) ]

    for dt in dates:
        r = ratio(sf_old(dt-days), sf(dt))
        if core.is_valid_num(r):
            outv[dt - fd] = r

    name = "mo_days({},{})".format(abbreviate(s),days)
    return core.vector_series(outv, fd, name=name)
        
    
    
    

#=================================

from common_testing_base import CommonTestingBase, obs_to_series
from private.test_support import MO_DAYS_200_OBS

class EMATest(CommonTestingBase):

    def test_ema_3(self):
        MO_DAYS_200_SERIES = obs_series.obs_to_series(MO_DAYS_200_OBS)
        f1 = MO_DAYS_200_SERIES.f
        f2 = mo_days(self.TEST_SERIES,200).f
        for dt in core.current_dates():
            self.assertEqual(f1(dt),f2(dt))


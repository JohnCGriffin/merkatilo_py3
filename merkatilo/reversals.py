
__all__ = [ 'reversals' ]

import merkatilo.core as core
from merkatilo.first_last_ob import first_ob
from merkatilo.private.abbreviate import abbreviate


def reversals(s, down_factor=1.0, up_factor=1.0, dates=None):
    '''When a series ascends above up-factor multiplied by a preceding 
    local minimum, a buy (1) signal is produced.  Upon 
    descending below the product of a local maximum and down-factor, 
    a sell (-1) signal is produced.
    '''
    dates = dates or core.current_dates()
    fd,ld = core.first_date(dates),core.last_date(dates)
    outv = [ None for dt in range(fd, ld+1) ]
    min_ob = max_ob = first_ob(s,dates)
    sf = s.f
    state = None

    for dt in dates:
        
        val = sf(dt)
        if not core.is_valid_num(val):
            continue
        
        if val > max_ob[1]:
            max_ob = (dt,val)
        if val < min_ob[1]:
            min_ob = (dt,val)

        if (1 != state) and (val > min_ob[1] * up_factor):
            max_ob = min_ob = (dt,val)
            outv[dt - fd] = 1
            state = 1
            
        elif (-1 != state) and (val < max_ob[1] * down_factor):
            max_ob = min_ob = (dt,val)
            outv[dt - fd] = -1
            state = -1

    return core.vector_series(outv, fd, name="reversals({})".format(abbreviate(s)))


#---------------------------------------------
from merkatilo.common_testing_base import CommonTestingBase, obs_to_series
from merkatilo.private.test_support import REVERSALS_95_105_OBS


class ReversalsTest(CommonTestingBase):

    def test_ema_3(self):
        REVERSALS_95_105_SERIES = obs_to_series(REVERSALS_95_105_OBS)
        self.verify_two_series(reversals(self.TEST_SERIES,up_factor=1.05,down_factor=.95),
                               REVERSALS_95_105_SERIES)


            

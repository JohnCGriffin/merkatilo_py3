
__all__ = [ 'min_max_obs', 'max_ob', 'min_ob' ]

import merkatilo.core as core

def min_max_obs(s, dates=None):
    
    '''Return a 2-tuple of (dt,value) observations representing
    the points of minimum and maximum values respectively.'''
    
    dates = dates or core.current_dates()
    min_ob = None
    max_ob = None
    f = s.f

    for dt in dates:
        val = f(dt)
        if core.is_valid_num(val):
            if not min_ob:
                min_ob = max_ob = (dt,val)
            if min_ob[1] > val:
                min_ob = (dt,val)
            if max_ob[1] < val:
                max_ob = (dt,val)

    if not min_ob:
        raise Exception("no observations")

    return min_ob, max_ob

def min_ob(s, dates=None):
    '''Shortcut to :code:`min_max_obs(s...)[0]`'''
    return min_max_obs(s,dates=dates)[0]

def max_ob(s, dates=None):
    '''Shortcut to :code:`min_max_obs(s...)[1]`'''
    return min_max_obs(s,dates=dates)[1]




#===================================

from merkatilo.common_testing_base import CommonTestingBase

class MinMaxTests(CommonTestingBase):

    def testMin(self):
        ob = min_ob(self.TEST_SERIES)
        self.assertEqual(ob[0], core.to_jdate('2012-1-13'))
        
    def testMax(self):
        ob = max_ob(self.TEST_SERIES)
        self.assertEqual(ob[0], core.to_jdate('2014-9-18'))
        
        
        

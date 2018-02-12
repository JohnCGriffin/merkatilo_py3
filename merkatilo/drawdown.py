
__all__ = [ 'drawdown', 'drawdown_residual' ]

import functools
import merkatilo.core as core
from merkatilo.obs_series import series_to_obs

# Collect incremental forward max observations and
# incremental backward min observations.  Pair each
# max with its nearest following min and find the
# biggest difference

def drawdown(s, dates=None):

    '''drawdown returns a 2-tuple of (date,value) tuples representing the
    beginning and ending observation points in an input series resulting
    in the greatest decrease in value.  This answers the question "How much
    unrealized loss did this investment have?"'''

    dates = dates or core.current_dates()
    obs = series_to_obs(dates,s)

    acc = []
    for ob in reversed(obs):
        if (not acc) or (ob[1] < acc[-1][1]):
            acc.append(ob)
    reversed_mins = list(reversed(acc))

    acc = []
    for ob in obs:
        if (not acc) or (ob[1] >= acc[-1][1]):
            acc.append(ob)
    maxs = acc

    def find_following_min(mx_ob):
        for ob in reversed_mins:
            if ob[0] > mx_ob[0]:
                return ob
        return None

    def make_max_min_pair(mx_ob):
        mn_ob = find_following_min(mx_ob)
        return (mx_ob,mn_ob) if mn_ob else None

    def maximize_pair(a,b):
        a_diff = a[0][1] / a[1][1]
        b_diff = b[0][1] / b[1][1]
        return b if (b_diff > a_diff) else a

    pairs = list(filter(None, [ make_max_min_pair(mx_ob) for mx_ob in maxs ]))

    return functools.reduce(maximize_pair, pairs)


def drawdown_residual (s, dates=None):
    dd = drawdown(s, dates=dates)
    return (dd[1][1] / dd[0][1])
    
#==================================
from merkatilo.common_testing_base import CommonTestingBase

class DrawdownTests(CommonTestingBase):

    def testDrawdown(self):
        dd = drawdown(self.TEST_SERIES)
        mx = (core.to_jdate('2014-9-18'), 361)
        mn = (core.to_jdate('2014-12-16'), 321)
        self.assertEqual(dd, (mx,mn))

    def testResidual(self):
        self.assertEqual(drawdown_residual(self.TEST_SERIES), 321/361)


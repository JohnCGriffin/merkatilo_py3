
__all__ = [ 'series_drawdown' ]

import functools
import merkatilo.core as core
from merkatilo.obs_series import series_to_obs

# Collect incremental forward max observations and
# incremental backward min observations.  Pair each
# max with its nearest following min and find the
# biggest difference

class drawdown(object):
    def __init__(self, max, min):
        self.max = max
        self.min = min
    def residual(self):
        return self.min[1] / self.max[1]
    def __repr__(self):
        return '<drawdown:{}..{}:{}>'.format(core.jdate_to_text(self.max[0]),
                                             core.jdate_to_text(self.min[0]),
                                             (1 - self.residual()))
            
def series_drawdown(s, dates=None):

    '''series_drawdown returns a drawdown object containing the
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
        if (not acc) or (ob[1] > acc[-1][1]):
            acc.append(ob)
    maxs = acc

    def find_following_min(mx_ob):
        for ob in reversed_mins:
            if ob[0] > mx_ob[0]:
                return ob
        return None

    def make_drawdown(mx_ob):
        mn_ob = find_following_min(mx_ob)
        return drawdown(mx_ob,mn_ob) if mn_ob else None

    def more_drawdown(a,b):
        return a if (a.residual() < b.residual()) else b

    pairs = list(filter(None, [ make_drawdown(mx_ob) for mx_ob in maxs ]))

    return functools.reduce(more_drawdown, pairs) if len(pairs) else None


def series_drawdowns(s, *, max_residual=1.0, dates=None):

    '''series_drawdowns returns all non-overlapping drawdowns,
       constrained by max_residual.  The result is ordered
       by the residual, i.e. worst drawdown first.'''

    dates = dates or core.current_dates()
    if(len(dates.vec) < 2):
        return []
    dd = series_drawdown(s, dates=dates)
    if not dd or (dd.residual() > max_residual):
        return []
    dd_left = series_drawdowns(s, max_residual=max_residual, dates=core.dates(dates,last=dd.max[0])) or []
    dd_right = series_drawdowns(s, max_residual=max_residual, dates=core.dates(dates,first=dd.min[0])) or []
    return sorted(dd_left + [ dd ] + dd_right, key=lambda a:a.residual())
    
    

#==================================
from merkatilo.common_testing_base import CommonTestingBase,approx

class DrawdownTests(CommonTestingBase):

    def testDrawdown(self):
        dd = series_drawdown(self.TEST_SERIES)
        mx = (core.to_jdate('2014-9-18'), 361)
        mn = (core.to_jdate('2014-12-16'), 321)
        test_dd = drawdown(mx,mn)
        self.assertEqual(dd.max, test_dd.max);
        self.assertEqual(dd.min, test_dd.min);

    def testResidual(self):
        self.assertEqual(series_drawdown(self.TEST_SERIES).residual(), 321/361)

    def testDrawdowns(self):
        dds = series_drawdowns(self.TEST_SERIES, max_residual=1.0)
        self.assertEqual([ approx(dd.residual()) for dd in dds[:3]],
                         [ approx(n) for n in [ 0.889196675900277, 0.9038461538461539, 0.9046052631578947]])


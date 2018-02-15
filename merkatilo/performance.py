
__all__ = [ 'gpa', 'investment_performance' ]

import merkatilo.core as core
from merkatilo.first_last_ob import first_ob, last_ob
from merkatilo.constant import constant
from merkatilo.signals import to_signals
from merkatilo.drawdown import drawdown_residual
from merkatilo.volatility import volatility
from merkatilo.equity_line import equity_line
from merkatilo.repeated import repeated
from merkatilo.series_count import series_count
from merkatilo.series_binop import gt


def gpa(s, dates=None):
    '''calculate the annualized gain of series s over dates.'''
    dates = dates or core.current_dates()
    early = first_ob(s,dates=dates)
    late = last_ob(s,dates=dates)
    days = late[0] - early[0]
    years = days / 365.2425
    gain = late[1] / early[1]
    return (gain ** (1 / years)) - 1

def long_ratio(signals):
    filled = repeated(signals, repeat_last=True)
    longs = series_count(gt(filled,0))
    total = series_count(filled)
    return longs/total

class Performance(object):
    
    '''Performance contains a few interesting facts about an equity line such as
    its drawdown and annualized gain.'''
    
    def __init__(self,*,
                 volatility_residual=None,
                 drawdown_residual=None,
                 annualized=None,
                 long_ratio=None,
                 signal_count=None):
        if not volatility_residual:
            raise Exception("missing volatility_residual")
        if not drawdown_residual:
            raise Exception("missing drawdown_residual")
        if not annualized:
            raise Exception("missing annualized")
        self.volatility_residual = volatility_residual
        self.drawdown_residual = drawdown_residual
        self.annualized = annualized
        self.signal_count = signal_count
        self.long_ratio = long_ratio
        
    def __repr__(self):
        return "(vr {:.3f}, dr {:.3f}, gpa {:.3f}, lng {}, sigs {})".format(
            self.volatility_residual,
            self.drawdown_residual,
            self.annualized,
            "{:.3}".format(self.long_ratio) if self.long_ratio else None,
            self.signal_count)
                 

def investment_performance(s,*, alternate_investment=None, signals=None, dates=None):
    
    '''Return interesting facts about an investment in a Performance object.'''
    
    dates = dates or core.current_dates()
    alternate_investment = alternate_investment or constant(1)
    signals = signals and to_signals(signals)

    with core.date_scope(dates):

        equity = equity_line(s,signals,alternate_investment=alternate_investment) if signals else s

        vol_res = 1 - volatility(equity)
        dd_res = drawdown_residual(equity)
        annualized = gpa(equity)

        return Performance(volatility_residual=vol_res,
                           drawdown_residual=dd_res,
                           annualized = annualized,
                           long_ratio = (long_ratio(signals) if signals else None),
                           signal_count=(signals and series_count(signals)))
                


#=====================================
from merkatilo.common_testing_base import *

class PerfTest(CommonTestingBase):

    def testGPA(self):
        self.assertEqual(approx(gpa(self.TEST_SERIES)), approx(0.07688365986138823))


    

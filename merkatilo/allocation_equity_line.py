
__all__ = [ 'allocation_equity_line' ]

import merkatilo.core as core
from merkatilo.constant import constant
from merkatilo.private.series_dates_values import series_dates_values
from merkatilo.first_last_ob import first_ob


class Portion(object):
    def __init__(self,series,amount):
        if not isinstance(series,core.series):
            raise Exception("first argument to Portion constructor must be series")
        if not (amount > 0):
            raise Exception("second argument to Portion constructor must be positive real")
        self.series = series
        self.amount = amount

def is_list_of(ob, t):
    if not isinstance(ob,list):
        return False
    for item in ob:
        if not isinstance(item,t):
            return False
    return True

class Allocation(object):
    def __init__(self, date, portions):
        if not is_list_of(portions, Portion):
            raise Exception("second argument to Allocation should be list of Portion")
        self.date = core.to_jdate(date)
        self.portions = portions

CASH = constant(1)

def normalize_allocation(a):
    total = sum([p.amount for p in a.portions])
    new_portions = ([ Portion(p.series,p.amount/total) for p in a.portions ] if total
                    else [ Portion(CASH,1) ])
    return Allocation(a.date, new_portions)

class Holding(object):
    def __init__(self, series, shares):
        if not isinstance(series, core.series):
            raise Exception("first argument to Holding should be series")
        if not (shares > 0):
            raise Exception("second argument to Holding should be positive real")
        self.series = series
        self.shares = shares

class Portfolio(object):
    def __init__(self, date, holdings):
        if not is_list_of(holdings, Holding):
            raise Exception("second argument to Allocation should be list of Portion")
        self.date = core.to_jdate(date)
        self.holdings = holdings
                

def value_of_holdings (date, holdings):
    total = 0
    for h in holdings:
        price = h.series.f(date)
        if not core.is_valid_num(price):
            return None
        total = total + (h.shares * price)
    return total
    

def allocations_to_portfolios(allocations):

    allocations = sorted([normalize_allocation(a) for a in allocations],
                         key=lambda a:a.date)

    holdings = [ Holding(CASH,1) ]

    result = []

    for a in allocations:

        date = a.date
        
        valuation = value_of_holdings(date, holdings)

        holdings = []

        for p in a.portions:
            f = p.series.f
            price = f(date)
            if not core.is_valid_num(price):
                raise Exception("missing price at {}".format(jdate_to_text(date)))
            dollars_for_buy = p.amount * valuation
            shares_to_buy = dollars_for_buy / price
            holdings.append(Holding(p.series,shares_to_buy))

        result.append(Portfolio(date, holdings))

    return result


def allocation_equity_line (allocations,*,initial_value=100):

    portfolios = allocations_to_portfolios(allocations)

    holdings_by_date = { p.date:p.holdings for p in portfolios }

    fd = portfolios[0].date

    holdings = [ Holding(CASH,1) ]

    obs = []

    for dt in range(fd, core.today(1)):

        valuation = value_of_holdings(dt, holdings)

        new_holdings = holdings_by_date.get(dt)

        if new_holdings:
            if not valuation:
                raise Exception("missing observation at allocate date {}".format(jdate_to_text(dt)))
            holdings = new_holdings

        if core.is_valid_num(valuation) and valuation > 0:
            obs.append((dt, initial_value * valuation)) 

    return obs_to_series(obs)



#=================================

from merkatilo.common_testing_base import CommonTestingBase, obs_to_series
from merkatilo.private.test_support import AAA_SERIES_OBS, BBB_SERIES_OBS
from merkatilo.series_binop import add, mul
from merkatilo.calibrate import calibrate


class EMATest(CommonTestingBase):

    def test_ema_3(self):
        AAA_SERIES = obs_to_series(AAA_SERIES_OBS)
        BBB_SERIES = obs_to_series(BBB_SERIES_OBS)
        core.set_dates(AAA_SERIES)
        allocations = [ Allocation(core.first_date(), [ Portion(AAA_SERIES,1234), Portion(BBB_SERIES, 1234) ]) ]
        self.verify_two_series(mul(allocation_equity_line(allocations), 2),
                               add(calibrate(AAA_SERIES) , calibrate(BBB_SERIES)))
        

            

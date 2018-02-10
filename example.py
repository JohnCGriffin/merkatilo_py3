
from user_imports import *
from performance import investment_performance

SPY = lo('SPY')

current_dates(dates(SPY))

print(investment_performance(SPY))
print(investment_performance(SPY, signals=mo(SPY,200)))

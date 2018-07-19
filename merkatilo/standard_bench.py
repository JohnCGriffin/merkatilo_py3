
from user_imports import *

import merkatilo.core as core
import time
from private.test_support import BENCHMARK_OBS
from obs_series import obs_to_series
from drawdown import series_drawdown

def measure(name, thunk):
    start = time.time()
    for i  in range(10):
        v = thunk()
        f = v.f
        for dt in core.current_dates():
            f(dt)
    elapsed = time.time() - start
    print('{} {}'.format(name, int(10.0 / elapsed)))
            
def standard_bench():
    bm = obs_to_series(BENCHMARK_OBS)
    core.set_dates(bm)
    reusable_ema = ema(bm,10)
    sigs = cross(slower=reusable_ema,faster=bm)
    measure("conviction", lambda: conviction(sigs,2))
    measure("cross", lambda: cross(slower=reusable_ema,faster=bm))
    measure("dd", lambda: (series_drawdown(bm) and bm))
    measure("ema", lambda: ema(bm,10))

if __name__ == "__main__":
    standard_bench()


'''

conviction  	2873
cross       	3396
dd          	6643
ema         	4952
equity      	2252
fudge       	7686
ma          	3364
math-add    	3661
math-div    	5102
math-mul    	3763
math-sub    	3761
min-max     	5949
mo          	2650
mo-days     	1605
prepend     	3136
repeated    	3943
reversal    	4067
signals     	4683
unrepeated  	4059
volatility  	1271
warp        	5263
'''


__all__ = [ 'series_map' ]

import core, obs_series, constant


def convert(s):
    if core.is_valid_num(s):
        return constant.constant(s)
    else:
        return s
        
    
def series_map(proc, *seriesz, missing_data_permitted=False, dts=None):
    
    def missing_nums(nums):
        return len(nums) != sum((1 for n in nums if core.is_valid_num(n)))
    
    converted = [ convert(s) for s in seriesz ]
    dts = dts or dates.current_dates()
    sfs = [ s.f for s in converted ]
    obs = []
    
    for dt in dts:
        nums = [ f(dt) for f in sfs ]
        if (not missing_data_permitted) and missing_nums(nums):
            continue
        val = proc(*nums)
        if core.is_valid_num(val):
            obs.append((dt,val))

    return obs_series.obs_to_series(obs)
    

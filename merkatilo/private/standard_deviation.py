
__all__ = [ 'standard_deviation' ]

import numbers, statistics

# It's worth noting that pstdev is population stdev, whereas
# statistics.stdev is for samples.

def standard_deviation (nums):
    cleaned = [ n for n in nums if (isinstance(n,numbers.Number) and n == n) ]
    return statistics.pstdev(cleaned)



__all__ = [ 'standard_deviation' ]

import numbers

def standard_deviation (nums):
    cleaned = [ n for n in nums if (isinstance(n,numbers.Number) and n == n) ]
    avg = sum(cleaned) / len(cleaned)
    sum_of_squared_diffs = sum([ (n - avg)**2 for n in cleaned ])/len(cleaned)
    return sum_of_squared_diffs ** .5

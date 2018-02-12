

import numbers

#####################################################
# IMPORTANT NOTE: SIGNAL VALUE AT ZERO
#
# A signal input is either negative or non-negative.
# Negative begets -1 and otherwise 1.  Zero is not
# a special case.
######################################################


def signalify_vector_copy (nums):
    copy = [ None for n in nums ]
    prev = None
    for (ndx,n) in enumerate(nums):
        if isinstance(n,numbers.Number):
            # SEE THE NOTE ABOVE
            sig = -1 if n < 0 else 1
            if sig != prev:
                copy[ndx] = sig
            prev = sig
    return copy
            

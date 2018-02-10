
__all__ = [ 'abbreviate' ]

import core

def abbreviate (item):
    text = item.name if (isinstance(item,core.series) and item.name) else "{}".format(item)
    return '...' if (len(text) > 30) else text


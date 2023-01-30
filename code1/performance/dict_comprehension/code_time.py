import operator
import collections
def identity(x):
    """ Identity function. Return x
    >>> identity(3)
    3
    """
    return x
def getter(index):
    if isinstance(index, list):
        if len(index) == 1:
            index = index[0]
            return lambda x: (x[index],)
        elif index:
            return operator.itemgetter(*index)
        else:
            return lambda x: ()
    else:
        return operator.itemgetter(index)
def groupby(key, seq):

    if not callable(key):
        key = getter(key)
    d = collections.defaultdict(lambda: [].append)
    for item in seq:
        d[key(item)](item)
    rv = {}
    for k, v in d.items():
        rv[k] = v.__self__
    return rv
data = list(range(1000)) * 1000
groupby(identity, data)
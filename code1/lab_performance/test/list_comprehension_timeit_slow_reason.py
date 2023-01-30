import timeit,itertools

import time
import gc

it = itertools.repeat(None, 100)
'''
gcold = gc.isenabled()
gc.disable()
start=time.perf_counter()
for _i in it:
    l = [e_0 for e_0 in x_0]
    pass
end = time.perf_counter()
print("*********zejun test total time pythonic**************", end - start)
'''
'''
def inner(_it, _timer):
    x_0 = list(range(1,11))*1000000
    _t0 = _timer()
    for _i in _it:
        l = [e_0 for e_0 in x_0]
        pass
    _t1 = _timer()
    print("*********zejun test total time pythonic**************", _t1 - _t0)
    return _t1 - _t0
timing = inner(it, time.perf_counter)
'''
'''
def inner(_it, _timer):
    x_0 = list(range(1,11))*1000000
    _it = itertools.repeat(None, 100)
    _timer=time.perf_counter
    _t0 = _timer()
    for _i in _it:
        l = [e_0 for e_0 in x_0]
        pass
    _t1 = _timer()
    print("*********zejun test total time pythonic**************", _t1 - _t0)
    return _t1 - _t0
'''
def inner(_it, _timer):
    x_0 = list(range(1,11))*1000000
    _it = itertools.repeat(None, 100)
    # _timer=time.perf_counter
    _t0 = time.perf_counter()
    for _i in _it:
        l = [e_0 for e_0 in x_0]
        pass
    _t1 = time.perf_counter()
    print("*********zejun test total time pythonic**************", _t1 - _t0)
    return _t1 - _t0
#timing = inner(it, time.perf_counter)
x_0 = list(range(1, 11)) * 100000
_it = itertools.repeat(None, 100)
# _timer=time.perf_counter
_t0 = time.perf_counter()
for _i in _it:
    l = [e_0 for e_0 in x_0]
    pass
_t1 = time.perf_counter()
print("*********zejun test total time pythonic**************", _t1 - _t0)

print("code is finished")
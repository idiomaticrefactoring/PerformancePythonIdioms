import timeit,itertools
import gc
import time
import dis
it = itertools.repeat(None, 100)
'''
x_0 = list(range(1,11))*1000000
gcold = gc.isenabled()
gc.disable()
start=time.perf_counter()
for _i in it:
    l = []
    for e_0 in x_0:
        l.append(e_0)
    pass
end = time.perf_counter()
print("*********zejun test total time**************",end-start)
'''
'''
def inner(_it, _timer):
    x_0 = list(range(1,11))*1000000
    _t0 = _timer()
    for _i in _it:
        l = []
        for e_0 in x_0:
            l.append(e_0)
        pass
    _t1 = _timer()
    print("*********zejun test total time**************", _t1 - _t0)
    return _t1 - _t0
'''
'''
def inner(_it, _timer):
    x_0 = list(range(1,11))*100000
    _it = itertools.repeat(None, 100)
    _timer = time.perf_counter
    _t0 = _timer()
    for _i in _it:
        l = []
        for e_0 in x_0:
            l.append(e_0)
        pass
    _t1 = _timer()
    print("*********zejun test total time**************", _t1 - _t0)
    return _t1 - _t0
'''
#'''
def inner(_it, _timer):

    x_0 = list(range(1,11))*100000
    _it = itertools.repeat(None, 100)
    # _timer = time.perf_counter
    _t0 = time.perf_counter()
    for _i in _it:
        l = []
        for e_0 in x_0:
            l.append(e_0)
        pass
    _t1 = time.perf_counter()
    print("*********zejun test total time**************", _t1 - _t0)
    return _t1 - _t0
#'''
# timing = inner(it, time.perf_counter)
#
# x_0 = list(range(1,11))*100000
# _it = itertools.repeat(None, 300)
# _t0 = time.perf_counter()
# for _i in _it:
#     l = []
#     for e_0 in x_0:
#         l.append(e_0)
#     pass
# _t1 = time.perf_counter()
# print("*********zejun test total time**************", _t1 - _t0)
#
# print("code is finished")
if __name__ == '__main__':
    timing = inner(it, time.perf_counter)
    dis.dis(inner)
    x_0 = list(range(1, 11)) * 100000
    _it = itertools.repeat(None, 100)
    _t0 = time.perf_counter()
    for _i in _it:
        l = []
        for e_0 in x_0:
            l.append(e_0)
        pass
    _t1 = time.perf_counter()
    print("*********zejun test total time**************", _t1 - _t0)
    dis.dis("list_comprehension_complicated_timeit_slow_reason.py")
    print("code is finished")
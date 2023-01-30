import itertools
import gc
import sys
import time
template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        {stmt}
        pass
    _t1 = _timer()
    return _t1 - _t0
"""
if __name__ == "__main__":
    setup="x_0 = list(range(1,11))*1000000"
    stmt="l = [e_0 for e_0 in x_0]"
    init = ''
    local_ns = {}
    _globals = globals
    global_ns = _globals()
    timer=time.perf_counter
    print(global_ns)
    dummy_src_name = "<timeit-src>"

    src = template.format(stmt=stmt, setup=setup, init=init)
    code = compile(src, dummy_src_name, "exec")
    print(code)
    exec(code, global_ns, local_ns)
    print("local_ns: ",local_ns)
    inner = local_ns["inner"]
    print(inner)

    it = itertools.repeat(None, 10)
    gcold = gc.isenabled()
    gc.disable()
    try:
        timing = inner(it, timer)
    finally:
        if gcold:
            gc.enable()
    # return timing
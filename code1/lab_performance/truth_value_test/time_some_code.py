def func_a():
    sum_time=0
    for i in range(10**3):
        if i<3:
            continue
        a = 0j
        import time
        start_time_zejun = time.perf_counter()
        if a == 0j:
            pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        sum_time += total_time_zejun
        # print('\n*********zejun test total time************** ', total_time_zejun)
        if a == 0j:
            pass
    print('\n*********zejun test total time************** ', sum_time)
def func_a_pythonic():
    sum_time=0
    for i in range(10**3):
        if i<3:
            continue
        a = 0j
        import time
        start_time_zejun = time.perf_counter()
        if not a:
            pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        sum_time+=total_time_zejun
        # print('\n*********zejun test total time pythonic************** ', total_time_zejun)
        if a == 0j:
            pass
    print('\n*********zejun test total time pythonic************** ', sum_time)


if __name__ == '__main__':
    func_a_pythonic()
    func_a()

    print('code is finished')
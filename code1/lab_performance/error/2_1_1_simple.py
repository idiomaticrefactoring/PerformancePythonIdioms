x_0 = list(range(1, 11)) * 100
x_1 = list(range(1, 11)) * 100
import time
for i in range(10000):

    start_time_zejun = time.perf_counter()
    l = []
    end_time_zejun = time.perf_counter()
    total_time_zejun = end_time_zejun - start_time_zejun
    start_time_zejun = time.perf_counter()
    l = [e_0 if e_0 % 2 else e_0 for e_0 in x_0 for e_1 in x_1 if e_0]
    end_time_zejun = time.perf_counter()
    total_time_zejun = end_time_zejun - start_time_zejun
    print('\n*********zejun test total time pythonic************** ', total_time_zejun)
print('len: ', len(l))
print('code is finished')
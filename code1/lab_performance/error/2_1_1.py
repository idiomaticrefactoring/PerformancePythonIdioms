x_0 = list(range(1, 11)) * 100
x_1 = list(range(1, 11)) * 100
import time
all_iter_time=0
for i in range(1000):

    start_time_zejun = time.perf_counter()
    l = []
    # end_time_zejun = time.perf_counter()
    # total_time_zejun = end_time_zejun - start_time_zejun
    # start_time_zejun = time.perf_counter()
    for e_0 in x_0:
        for e_1 in x_1:
            if e_0:
                if e_0 % 2:
                    l.append(e_0)
                else:
                    l.append(e_0)
    end_time_zejun = time.perf_counter()
    total_time_zejun = end_time_zejun - start_time_zejun
    all_iter_time+=total_time_zejun
    print('\n*********zejun test total time************** ', total_time_zejun)
print('len: ', len(l))
print('code is finished')
print(all_iter_time)
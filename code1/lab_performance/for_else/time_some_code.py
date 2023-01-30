import time
import dis

def func_a():
    sum_time=0
    for i in range(10**3):
        if i<3:
            continue
        a = 0j
        e_list = [i for i in range(1000000)]
        start_time_zejun = time.perf_counter()
        flag = True
        for i in e_list:
            if i == 999999:
                flag = False
                break
        if flag == True:
            pass
        # print('code is finished')
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
        e_list = [i for i in range(1000000)]
        start_time_zejun = time.perf_counter()
        for i in e_list:
            if i == 999999:
                break
        else:
            pass
        # print('code is finished')
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
    dis.dis(func_a)
    dis.dis(func_a_pythonic)
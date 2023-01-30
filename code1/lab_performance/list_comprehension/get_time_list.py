import time
import sys,ast,os
import tokenize
import traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+'extract_transform_complicate_code_new/')
sys.path.append(code_dir+'extract_transform_complicate_code_new/comprehension/')
import util
bench_dir=util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
file_path="4_0_0_list(range(1,11))_func.py"
content = util.load_file_path(bench_dir+file_path)
print(content)
def func_a():
    repeat=10**5
    total_time = 0
    length=10**4+1
    for i in range(repeat):
        if i<3:
            continue
        x_0 = list(range(1, length))
        x_1 = list(range(1, 11))
        x_2 = list(range(1, 11))
        x_3 = list(range(1, 11))
        l = []
        start_time_zejun = time.perf_counter()
        for e_0 in x_0:
            l.append(e_0)
        # for e_0 in x_0:
        #     for e_1 in x_1:
        #         for e_2 in x_2:
        #             for e_3 in x_3:
        #                 l.append(e_0)
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time += total_time_zejun
    print('func code is finished: ', total_time)
    total_time_pythonic = 0

    for i in range(repeat):
        if i<3:
            continue
        x_0 = list(range(1, length))
        x_1 = list(range(1, 11))
        x_2 = list(range(1, 11))
        x_3 = list(range(1, 11))
        l = []
        start_time_zejun = time.perf_counter()
        l = [e_0 for e_0 in x_0]
        # l = [e_0 for e_0 in x_0 for e_1 in x_1 for e_2 in x_2 for e_3 in x_3]
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        total_time_pythonic += total_time_zejun
    print('func code is finished: ', total_time_pythonic,total_time/total_time_pythonic)

    # print('len: ',len(l))
    # print('code is finished')
if __name__ == '__main__':
    func_a()
'''
total_time = 0
for i in range(35):
    start_time_zejun = time.perf_counter()
    for e_0 in x_0:
        for e_1 in x_1:
            for e_2 in x_2:
                for e_3 in x_3:
                    l.append(e_0)
    # five_2 == e == five in a_list
    end_time_zejun = time.perf_counter()
    total_time_zejun = end_time_zejun - start_time_zejun
    total_time += total_time_zejun
print('func code is finished: ',total_time)
'''
import time
import traceback

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy
import matplotlib.pyplot as plt
import subprocess
import pandas as pd

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_list_comprehension
import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util,util_perf
from lab_code_info import LabCodeInfo
def func_a():
    m = 109
    n = 110
    p = 112
    p_copy = [p]
    o = 111

    n >= m and m != n and (n != o) and (o not in [p]) and ([p] is p_copy)
    print(n >= m and m != n and (n != o) and (o not in [p]) and ([p] is p_copy))

    p = 112
    o = 111
    n = 110
    n is not o and o is not p
    print(n is not o and o is not p)
    n = 110
    m = 109
    o = 111
    n >= m and m != n and (n not in [o]) and ([o] not in [[o]]) and ([[o]] is not [[o]])
    print(n >= m and m != n and (n not in [o]) and ([o] not in [[o]]) and ([[o]] is not [[o]]))

    n = 110
    list_0 = [n]
    list_1 = [n]
    list_2 = [list_1]
    list_3 = [n]
    list_4 = [list_3]
    list_5 = [list_4]
    list_6 = [n]
    list_7 = [list_6]
    list_8 = [list_7]
    list_9 = [list_8]
    n in list_0 and list_0 in list_2 and (list_2 in list_5) and (list_5 in list_9)
    print(n in list_0 and list_0 in list_2 and (list_2 in list_5) and (list_5 in list_9))
    print(list_1 is list_0)
if __name__ == '__main__':
    def func_a():
        for i in range(35):


            a = set(1)
            try:
                import time
                start_time_zejun = time.perf_counter()
                assert a == set()
                end_time_zejun = time.perf_counter()
                total_time_zejun = end_time_zejun - start_time_zejun
                print('\n*********zejun test total time************** ', total_time_zejun)
                assert a == set()
            except:
                pass



    func_a()
    print('code is finished')
    # func_a()
    # bench_dir = util.data_root + "lab_performance/chain_compare_benchmarks_new/code/code/"
    # bench_dir = util.data_root_mv + "lab_performance/truth_value_test_benchmarks/code/code/"
    #
    # dir_list=os.listdir(bench_dir)
    # for file_name in dir_list[:]:  # 9001750
    #     # if file_name!="0_!=_!=_<_not in_is_func.py":#"0_!=_!=_!=_!=_!=_func.py":
    #     #     continue
    #     if file_name!="0j_empty_==_equal_flag_if_node_func.py":
    #         continue
    #     content = util.load_file_path(bench_dir+file_name)
    #     print(content)


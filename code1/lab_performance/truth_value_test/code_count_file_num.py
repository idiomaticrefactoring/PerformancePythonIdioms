import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
sys.path.append(code_dir+"lab_performance")
sys.path.append(code_dir+"wrap_refactoring/")
from truth_value_test import performance_replace_content_by_ast_time_percounter

import refactor_truth_value_test
import lab_performance_util
import util
from lab_code_info import LabCodeInfo
if __name__ == '__main__':
    bench_time_info_dir=util.data_root_mv + "lab_performance/truth_value_test_benchmarks/bench_time_info_dir_prefined_cpu_new_2/"
    bench_dir = util.data_root_mv + "lab_performance/truth_value_test_benchmarks/code/code/"
    file_name_list=[]
    for file_name in os.listdir(bench_dir):
        file_name_no_suffix=file_name[:-3]
        file_name_list.append(file_name_no_suffix)
    file_name_list_2=[]
    for file_name in os.listdir(bench_time_info_dir):
        file_name_no_suffix = file_name[:-4]
        file_name_list_2.append(file_name_no_suffix)
    set_1=set(file_name_list) - set(file_name_list_2)
    print("cha",file_name_list[0],len(file_name_list),len(file_name_list_2),len(set_1))
    print("total",set(file_name_list) - set(file_name_list_2))




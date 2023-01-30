import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_chain_compare
import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util
from lab_code_info import LabCodeInfo
bench_dir = util.data_root + "lab_performance/chain_compare_benchmarks/code/code/"
bench_time_info_dir = util.data_root + "lab_performance/chain_compare_benchmarks/bench_time_info_dir_prefined_cpu_new/"

total_start_time=time.time()
prefined_cpu = "taskset -c 4,5 "
print("total number: ",len(os.listdir(bench_dir)))
import random
dir_list=list(os.listdir(bench_dir))
dir_list.sort()
for file_name in dir_list[:1]:  # 9001750
    # if file_name!="1_3_1_[1]_func.py":
    #     continue
    if os.path.exists(bench_time_info_dir + file_name[:-3] + ".pkl"):
        print(bench_time_info_dir + file_name, "is existed")
        continue

    code_list = refactor_chain_compare.refactor_chain_compare(bench_dir + file_name)
    print(code_list)
    for old_tree,new_tree in code_list:
        print("code: ",ast.unparse(old_tree),ast.unparse(new_tree))
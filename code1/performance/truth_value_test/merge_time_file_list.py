import sys, ast, os, csv, time, copy

import subprocess
import traceback

from pathos.multiprocessing import ProcessingPool as newPool

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import pandas as pd
import util, performance_util
from code_info import CodeInfo

if __name__ == '__main__':
    bench_time_info_dir_truth_test=util.data_root_mv+"performance/a_truth_value_test/a_truth_value_test_iter_invoca_total_data/"
    bench_time_info_dir_set_comp = util.data_root_mv + "performance/a_set_comprehension_2/set_comprehension_iter_invoca_2/"
    bench_time_info_dir=util.data_root+"performance/a_multi_assign_swap_new/a_multi_assign_iter_invoca/"

    bench_time_info_dir=util.data_root + "performance/a_multi_assign/a_multi_assign_iter_invoca/"
    bench_time_info_dir=util.data_root+"performance/a_multi_assign_swap_new/a_multi_assign_iter_invoca/"

    load_time_info=util.data_root_mv+"performance/total_time_dir/"
    total_time_list={
        "truth_value_test": bench_time_info_dir_truth_test
    }
    for key in total_time_list:
        print(f">>>>>>>>>>>>>>>>>>>>>>>>save {key} info")
        bench_time_info_dir=total_time_list[key]
        code_info_file_name=key+"truth_value_test_total_time_list"
        time_list=[]
        count_file_name=len(os.listdir(bench_time_info_dir)[:])
        success_file_name=0
        failed_file_name=0
        for ind, file_name in enumerate(sorted(os.listdir(bench_time_info_dir)[:])):
            try:
                file_name_no_suffix = file_name[:-4]
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
            except:
                print(f"the file {file_name} is wrong!")
                traceback.print_exc()
                failed_file_name+=1
                continue
            success_file_name+=1
            time_list.append(lab_code_info)
        util.save_pkl(load_time_info, code_info_file_name, time_list)
        print("count_file_name,success_file_name,failed_file_name: ",count_file_name,success_file_name,failed_file_name)


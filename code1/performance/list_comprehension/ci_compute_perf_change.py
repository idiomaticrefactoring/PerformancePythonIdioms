import sys, ast, os, csv, time, copy
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
print("code_dir: ",code_dir)
sys.path.append(code_dir+"performance/")
# from code_info import CodeInfo
import util, performance_util
from code_info import CodeInfo
from pathos.multiprocessing import ProcessingPool as newPool


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def save_perf_change(file_name):
    file_name_no_suffix = file_name[:-4]

    lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
    lab_code_info: CodeInfo
    file_html = lab_code_info.file_html
    # if "qubit_tapering_from_stabilizer.py" in file_html:
    #     print("come the file: ",file_html)
    # if file_html != "https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/transforms/repconversions/qubit_tapering_from_stabilizer.py":
    #     continue
    total_time_list_info_dict = lab_code_info.get_stable_time_list_tosem_2020()
    # print("total_time_list_info_dict: ",total_time_list_info_dict)
    # for invo in invo_list:
    lab_code_info.get_performance_info(total_time_list_info_dict=total_time_list_info_dict, invocations=50,
                                       steps=100, remove_outlier=remove_outlier,factor=1.5)
    # perf_info_dict = lab_code_info.total_time_list_info_dict
    # for test_me in perf_info_dict:
    #     for instance in perf_info_dict[test_me]:
    #         perf_info = perf_info_dict[test_me][instance]["perf_change"]
    #         if instance != 8:
    #             continue
    #         print("perf_info: ", file_name, test_me, instance, perf_info)
    util.save_pkl(save_code_info_dir_add_performance_change + "/", file_name_no_suffix,
                  lab_code_info)
    print("save successfully! ",save_code_info_dir_add_performance_change,file_name_no_suffix)

if __name__ == '__main__':
    bench_time_info_dir =util.data_root + "performance/list_compre_benchmarks_iter_invoca_6_4/"
    # bench_time_info_dir =util.data_root + "performance/list_compre_benchmarks_iter_invoca_6_4_2/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_2nd_invo_step_100/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_1st_invo_step_100/50/"
    save_code_info_dir_add_performance_change= \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_2_50_invocations/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_2_50_invocations/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_1.5factor/"

    factor=1.5
    remove_outlier = True
    file_name_list=[]
    for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
        file_name_list.append(file_name)
        '''
        file_name_no_suffix = file_name[:-4]

        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        # if "qubit_tapering_from_stabilizer.py" in file_html:
        #     print("come the file: ",file_html)
        # if file_html != "https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/transforms/repconversions/qubit_tapering_from_stabilizer.py":
        #     continue
        total_time_list_info_dict = lab_code_info.get_stable_time_list_tosem_2020()
        # print("total_time_list_info_dict: ",total_time_list_info_dict)
        # for invo in invo_list:
        lab_code_info.get_performance_info(total_time_list_info_dict=total_time_list_info_dict, invocations=50,
                                           steps=100,remove_outlier=remove_outlier)
        perf_info_dict = lab_code_info.total_time_list_info_dict
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                perf_info = perf_info_dict[test_me][instance]["perf_change"]
                if instance != 8:
                    continue
                print("perf_info: ", file_name, test_me, instance, perf_info)
        util.save_pkl(save_code_info_dir_add_performance_change + "/", file_name_no_suffix+str(remove_outlier), lab_code_info)
    '''
    print("len of file_name_list: ",len(file_name_list))
    pool = newPool(nodes=30)
    pool.map(save_perf_change, file_name_list[:])  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
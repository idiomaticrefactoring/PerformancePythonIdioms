import sys, ast, os, csv, time, copy
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import util,performance_util
from code_info import CodeInfo

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':

    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_1st_invo_step_100/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_1.5factor/"


    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_2_50_invocations/"

    save_code_info_dir_add_performance_change = \
        util.data_root +"performance/tosem_2020_list_compre_bench_rq_1_2nd_invo_step_100/50/"

    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        # lab_code_info_remove_outlier = util.load_pkl(save_code_info_dir_add_performance_change_remove_outlier, file_name_no_suffix)
        # perf_info_dict_remove_outlier= lab_code_info_remove_outlier.total_time_list_info_dict

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        if file_html!="https://github.com/HunterMcGushion/hyperparameter_hunter/tree/master/hyperparameter_hunter/space/space_core.py":#"https://github.com/cloud-custodian/cloud-custodian/tree/master/c7n/filters/iamaccess.py":#"https://github.com/HunterMcGushion/hyperparameter_hunter/tree/master/hyperparameter_hunter/space/space_core.py":#"https://github.com/in-toto/in-toto/tree/master/in_toto/runlib.py":#"https://github.com/gnebbia/kb/tree/master/kb/db.py":#"https://github.com/gugarosa/opytimizer/tree/master/opytimizer/optimizers/swarm/kh.py":
            continue
        code_str = lab_code_info.get_code_str()
        perf_info_dict = lab_code_info.total_time_list_info_dict
        for test_me in perf_info_dict:
            # if "test_lstrip_paths_substring_prefix_directory" not in test_me:
            #     continue
            if "test_space_consistency" not in test_me:
                continue
            # if "test_sqs_policies" not in test_me:
            #     continue
            for instance in perf_info_dict[test_me]:
                if instance==73:
                    total_time=perf_info_dict[test_me][instance]
                    time_list=total_time['time_list']
                    pythonic_time_list=total_time['pythonic_time_list']
                    print("time_list count,mean, median, min, max: ", len(time_list), np.mean(time_list),
                          np.median(time_list), np.min(time_list), np.max(time_list))
                    print("pythonic_time_list count,mean, median, min, max: ", len(pythonic_time_list), np.mean(pythonic_time_list),
                          np.median(pythonic_time_list), np.min(pythonic_time_list), np.max(pythonic_time_list))

                    plt.boxplot([ee for e in time_list for ee in e])
                    plt.show()
                    plt.boxplot([ee for e in pythonic_time_list for ee in e])
                    plt.show()
                    # print(total_time)

    '''
    # dict_pd=performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change)
    perf_improve_dict=performance_util.get_ci_perf_change_dict_add_num_ele_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)

    perf_improve_list=perf_improve_dict['perf_change']
    print("count,mean, median, min, max: ",len(perf_improve_list), np.mean(perf_improve_list), np.median(perf_improve_list), np.min(perf_improve_list), np.max(perf_improve_list))
    plt.boxplot(perf_improve_list)
    plt.show()
    '''


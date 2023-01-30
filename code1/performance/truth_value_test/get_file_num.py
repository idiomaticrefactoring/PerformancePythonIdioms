import sys, ast, os, csv, time, copy

import subprocess
from pathos.multiprocessing import ProcessingPool as newPool

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
print(code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir + "performance/")
import pandas as pd
import util, performance_util
# import code_info
from code_info import CodeInfo

# from code_info import CodeInfo
'''
Merge all Test Cases with time of Truth Value Test into  save_code_info_dir_mv directory
'''
if __name__ == '__main__':

    save_code_info_dir = util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca/"
    # save_code_info_dir = util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_some/"
    save_code_info_dir_mv=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_complete/"
    count_0=0
    count_1=0
    for file_name in os.listdir(save_code_info_dir):
        file_name=file_name[:-4]

        code_info = util.load_pkl(save_code_info_dir, file_name)
        code_info: CodeInfo
        all_invocations_time_list=code_info.simple_code_time_dict
        all_test_case_time_list_old=all_invocations_time_list[0]
        for key in all_test_case_time_list_old:
            if all_test_case_time_list_old[key]:
                # print(all_test_case_time_list_old)
                count_1+=1
                # util.save_pkl(save_code_info_dir_mv, file_name, code_info)

                break
        else:
            count_0+=1
            print(">>>>>>>>>>>>>>>It does not through the truth value test: ",file_name)
            # no_through_code_list.append(
            #     [ind_code, ind_code + offset, "complicated code", file_html, cl, me_name, total_name,
            #      total_name + "_" + str(ind_code + offset)])
            continue

    print("count: ",len(os.listdir(save_code_info_dir)),count_0,count_1)

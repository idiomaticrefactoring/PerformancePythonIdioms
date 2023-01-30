import time

import numpy as np
import sys, ast, os, csv, time, copy

import subprocess

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")

import util, performance_util
from code_info import CodeInfo

'''
# return dict_flag_stable each ele is stable flag in all instances of all test methods 
'''


def get_flag(time_dict):
    dict_flag_stable = dict()
    for i, e_invo in enumerate(time_dict):
        # print(e_invo)

        for test_me in e_invo:
            # if ('https://github.com/kellyjonbrazil/jc/tree/master/tests/test_csv.py', 'tests.test_csv', 'MyTests', 'test_csv_flyrna') !=test_me:
            #     continue
            # print("the file: ",test_me,e_invo[test_me])
            if test_me not in dict_flag_stable:
                dict_flag_stable[test_me] = dict()
            for ind_case, test_case_time in enumerate(e_invo[test_me]):
                # print(test_case_time)
                test_case_time = [float(e) for e in test_case_time]
                stable_flag = performance_util.whether_cov(test_case_time[3:], window)
                if ind_case not in dict_flag_stable[test_me]:
                    dict_flag_stable[test_me][ind_case] = 0
                dict_flag_stable[test_me][ind_case] += stable_flag
        # break
    print(dict_flag_stable)


if __name__ == '__main__':
    save_code_info_dir_add_performance_change = util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_1st_invo_step_100/"
    # save_code_info_dir_add_performance_change = util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_2nd_invo/"

    # save_code_info_dir_add_performance_change = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_2_tosem_2020_20invo/"#实际是20
    # save_code_info_dir_add_performance_change = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_tosem_2020_20invo/"#实际是20
    # list_compre_benchmarks_iter_improv_final_add_perf_change_test_2_tosem_2020_10invo
    # "performance/list_compre_benchmarks_iter_improv_final_test_30invo_2/",
    # "performance/list_compre_benchmarks_iter_improv_final_test_30invo/",
    # "performance/list_compre_benchmarks_iter_improv_final_test_20invo_2/",
    # "performance/list_compre_benchmarks_iter_improv_final_test_20invo/",
    # "performance/list_compre_benchmarks_iter_improv_final_test_2/",
    save_code_info_dir_add_performance_change_list=["performance/tosem_2020_list_compre_bench_rq_1_1st_invo_step_100/","performance/tosem_2020_list_compre_bench_rq_1_2nd_invo_step_100/"]
    bench_time_info_dir_list = [

        "performance/list_compre_benchmarks_iter_invoca_6_4/",
        "performance/list_compre_benchmarks_iter_invoca_6_4_2/",
        "performance/list_compre_benchmarks_iter_improv_final_test/",
        "performance/list_compre_benchmarks_iter_improv_final/",
        "performance/list_compre_benchmarks_new_test_single_file_final/", "performance/list_compre_benchmarks_new/",
        "performance/list_compre_benchmarks/"]  # code_base

    file_name_list = set([])
    total_code_num = 0
    total_code_instance_num = 0
    total_code_stable_num = 0
    total_code_instance_stable_num = 0

    total_code_stable_num_pythonic = 0
    total_code_instance_stable_num_pythonic = 0
    both_total_code_stable_num = 0
    both_total_code_instance_stable_num = 0
    invo_list=[10*(i+1) for i in range(5)]
    invo_list=[50]
    num_ele_num_dict = dict()
    total_time_invo_start = time.time()
    for ind_1,dir_e in enumerate(bench_time_info_dir_list[:2]):
        if ind_1==0:
            continue
        bench_time_info_dir = util.data_root + dir_e
        save_code_info_dir_add_performance_change=util.data_root +save_code_info_dir_add_performance_change_list[ind_1]
        # print(dir_e)
        print(f"total file of benchmarks in {bench_time_info_dir} is: ", len(os.listdir(bench_time_info_dir)))
        # file_name_list=[]

        for invo in invo_list:
            file_name_stable_list = []
            time_invo_start=time.time()
            for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                if os.path.exists(save_code_info_dir_add_performance_change + str(invo) + "/" + file_name):
                    continue

                # print("file_name: ",file_name)
                # break
                file_name_list.add(file_name)
                if file_name in file_name_stable_list:
                    continue
                # if ind>10:
                #     break
                # if file_name!="2_4_3_[1].pkl":#"1_1_0_list(range(1,11))*10.pkl":#
                #     continue
                file_name_no_suffix = file_name[:-4]
                file_path=save_code_info_dir_add_performance_change+str(invo)+"/"+file_name_no_suffix+".pkl"
                if os.path.exists(file_path):
                    continue
                print("file_name is not existed ",invo,file_path)
                #'''
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: CodeInfo
                total_time_list_info_dict = lab_code_info.get_stable_time_list_tosem_2020()
                # print("total_time_list_info_dict: ",total_time_list_info_dict)
                # for invo in invo_list:
                lab_code_info.get_performance_info(total_time_list_info_dict=total_time_list_info_dict, invocations=invo,steps=100)
                # print("performance change: ",lab_code_info.total_time_list_info_dict)
                util.save_pkl(save_code_info_dir_add_performance_change+str(invo)+"/", file_name_no_suffix, lab_code_info)
                # lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
                # print(">>>test load info>>>>>>>performance change: ",lab_code_info.total_time_list_info_dict)
                #'''
            time_invo_end = time.time()
            print(f"{invo} invocations' time: ",time_invo_end-time_invo_start)
                # break
    total_time_invo_end = time.time()
    print("total_time: ", total_time_invo_end - total_time_invo_start)

    print("num_ele_num_dict: ", num_ele_num_dict)
    '''
    {'119': 2, '2': 106, '1': 249, '87': 1, '18': 2, '11766': 1, '128': 1, '16': 5, '4': 13, '0': 84, '8': 15, '3': 44, '6': 14, '26': 1, '5': 52, '101': 1, '100': 2, '10': 16, '7': 2, '11': 1, '246': 1, '127': 1, '91': 1, '24': 1, '17': 1, '30': 1, '9': 1, '31': 2}
    '''
    # print(f"stable info:\ntotal_code_num: {total_code_num}, total_code_instance_num: {total_code_instance_num}\n"
    #       f"both_total_code_stable_num: {both_total_code_stable_num}, both_total_code_instance_stable_num: {both_total_code_instance_stable_num}\n"
    #       f"total_code_stable_num: {total_code_stable_num}, total_code_instance_stable_num: {total_code_instance_stable_num}\n"
    #       f"total_code_stable_num_pythonic: {total_code_stable_num_pythonic}, total_code_instance_stable_num_pythonic: {total_code_instance_stable_num_pythonic}")

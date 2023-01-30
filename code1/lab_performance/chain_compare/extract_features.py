import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

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

import pandas as pd
if __name__ == '__main__':
    bench_time_info_dir= \
        util.data_root + "lab_performance/chain_compare_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"

    # util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new_add_perf_change/50/"
        # util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new/"
    csv_feature_file_name_add_interval=util.data_root +"lab_performance/chain_compare_benchmarks/csv/lab_performance_features_chain_compare.csv"
    #cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

    dict_pd={'num_Eq': [],'num_NotEq': [],'num_Lt': [],'num_LtE': [],'num_Gt': [],'num_GtE': [],
             'num_Is': [], 'num_IsNot': [],'num_In': [],'num_NotIn': [],
             'num_cmpop': [],'perf_change': [], 'in_func': []}

    for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):

        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        print("file_name: ",file_name)

        # print("num_for, num_if, num_if_else, e_input: ",num_for, num_if, num_if_else, e_input)
        old_node, new_tree = lab_code_info.code_info
        dict_features = util_perf.get_features_chain_compare([old_node])  # .get_features()
        # for key in dict_features_old:
        #         dict_difference[key+"_diff"]=dict_features_old[key]-dict_features_new[key]
        perf_change=lab_code_info.perf_ci_info[0]
        dict_features['perf_change']=perf_change
        if perf_change>1.2:
            continue
        if "func" in file_name:
            dict_features['in_func']=1
        else:
            dict_features['in_func'] = 0
        # print(dict_features)

        for key in dict_pd:
            dict_pd[key].append(dict_features[key])
    #     break
    # print(dict_pd)
    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_add_interval, index=False)

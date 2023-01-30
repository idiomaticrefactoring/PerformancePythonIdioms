import time
import traceback

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
def save_features_add_interval(bench_time_info_dir):
    dict_pd = {"perf_change":[],"num_ele":[],'num_loop': [],
                   'num_if': [], 'num_if_else': [],
                   'context': []}

    # '''
    for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
        no_file_name = file_name[:-4]
        if no_file_name not in total_file_list:
            continue
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        print("file_name: ", file_name)
        for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
        dict_features_old = util_perf.get_features_list_comprehension([for_node, assign_node])  # .get_features()
        dict_difference = {"num_ele": int(lab_code_info.num_add_ele)}
        # for key in dict_features_old:
        #         dict_difference[key+"_diff"]=dict_features_old[key]-dict_features_new[key]
        dict_features = {**dict_difference, **dict_features_old}
        perf_change = lab_code_info.perf_ci_info[0]
        dict_pd['perf_change'].append(perf_change)
        if "_func" in file_name:
            dict_pd["context"].append("func")
        else:
            dict_pd["context"].append("Nfunc")
        # if "_func" in file_name:
        #     dict_pd["context"].append(1)
        # else:
        #     dict_pd["context"].append(0)

        # print(dict_features)

        for key in dict_features:
            dict_pd[key].append(dict_features[key])

    print("total num: ",len(dict_pd['perf_change']))
    dataMain = pd.DataFrame(data=dict_pd)
    for key in dataMain:
        feature=dataMain[key]
        # average=feature.mean()
        # std = feature.std()
        try:
            a=scipy.stats.skew(feature)
            print("skew: ",key,a)
        except:
            print("the key cannot compute the skew")
            traceback.print_exc()

    dataMain.to_csv(csv_feature_file_name_corr, index=False)

if __name__ == '__main__':
    bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    total_file_list = [e[:-3] for e in os.listdir(bench_dir)]

    bench_time_info_dir=\
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new_add_perf_change/50/"
        # util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new/"
    csv_feature_file_name_corr=util.data_root +"lab_performance/list_compre_benchmarks_fun_and_Nfunc/csv/list_compre_lab_performance_features.csv"

    save_features_add_interval(bench_time_info_dir)
    # dict_pd={'num_ele': [], 'num_loop': [],
    #                'num_if': [], 'num_if_else': [],
    #                'perf_change': [], 'in_func': []}
    #
    # for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
    #     no_file_name = file_name[:-4]
    #     if no_file_name in total_file_list:
    #         continue
    #     file_name_no_suffix = file_name[:-4]
    #     lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
    #     lab_code_info: LabCodeInfo
    #     print("file_name: ",file_name)
    #
    #     # print("num_for, num_if, num_if_else, e_input: ",num_for, num_if, num_if_else, e_input)
    #     for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
    #     dict_features_old = util_perf.get_features_list_comprehension([for_node, assign_node])  # .get_features()
    #     dict_difference = {"num_ele": int(lab_code_info.num_add_ele)}
    #     # for key in dict_features_old:
    #     #         dict_difference[key+"_diff"]=dict_features_old[key]-dict_features_new[key]
    #     dict_features = {**dict_difference, **dict_features_old}
    #     perf_change=lab_code_info.perf_ci_info[0]
    #     dict_features['perf_change']=perf_change
    #     if "func" in file_name:
    #         dict_features['in_func']=1
    #     else:
    #         dict_features['in_func'] = 0
    #     # print(dict_features)
    #
    #     for key in dict_pd:
    #         dict_pd[key].append(dict_features[key])
    #     # break
    # # print(dict_pd)
    # dataMain = pd.DataFrame(data=dict_pd)
    # dataMain.to_csv(csv_feature_file_name_add_interval, index=False)

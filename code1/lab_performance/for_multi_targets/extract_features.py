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
'''
1. node
    1.1 Instances of Subcript Node
    1.2 Num of Subscript: 1,….., 30
2. Context
3. Braches: None
4. Data:
Type: only constant
Size:1,10,100, …, 10e6
Dimension: 1, 2
'''
def save_features_add_interval(dict_perf_change):
    dict_pd = {"file_html":[],"code_str":[],"perf_change":[],
               "size_data":[],'num_subscript': [],'dim_subscript': [],
              "unpack_num":[],'context': [],"is_total_data":[],
               "num_star":[],"num_iter_unpack":[],"subs_unpack_ratio":[]}

    # '''
    dict_pd["file_html"]=dict_perf_change["file_html"]
    dict_pd["code_str"] = dict_perf_change["code_str"]
    for ind, file_name in enumerate(dict_perf_change["file_html"]):
        no_file_name = file_name[:-4]
        code_str=dict_perf_change["code_str"][ind]
        file_name_no_suffix = file_name[:-4]
        data_size = int(file_name_no_suffix.split("_")[2])
        unpack_num = int(file_name_no_suffix.split("_")[6])
        num_subscript = int(file_name_no_suffix.split("_")[8])
        #0_Endflag_20_num_0_lower_1_step_3_subscript_func
        dict_pd["num_star"].append(code_str.count("*"))
        dict_pd["num_iter_unpack"].append(code_str.count(",")+1)
        dict_pd["subs_unpack_ratio"].append(num_subscript/(code_str.count(",")+1))
        dict_pd["size_data"].append(data_size)
        dict_pd["unpack_num"].append(unpack_num)
        dict_pd["num_subscript"].append(num_subscript)
        if "2_dim" in file_name:
            dict_pd["dim_subscript"].append(2)
        else:
            dict_pd["dim_subscript"].append(3)

        if "0_flag" in file_name:
            dict_pd["is_total_data"].append("False")
        else:
            dict_pd["is_total_data"].append("True")

        if "_func" in file_name:
            dict_pd["context"].append("func")
        else:
            dict_pd["context"].append("Nfunc")

        perf_change = dict_perf_change["perf_change_zonghe"][ind]
        dict_pd['perf_change'].append(perf_change)

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
    # bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    # total_file_list = [e[:-3] for e in os.listdir(bench_dir)]

    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/for_multi_targets_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/for_multi_targets_benchmarks/prefined_cpus_remain_code_new_add_perf_change/50/"

    dict_pd = lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change)
    # dict_pd=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change_remove_outlier)


    # '''
    dict_pd_remove_outlier = lab_performance_util.get_ci_perf_change_dict(
        save_code_info_dir_add_performance_change_remove_outlier)
    for key in dict_pd_remove_outlier:
        if key not in ["file_html","code_str"]:
            dict_pd[key+"_rm_outlier"]=[]
    for file_html in dict_pd["file_html"]:
        index=dict_pd_remove_outlier["file_html"].index(file_html)
        for key in dict_pd_remove_outlier:
            if key not in ["file_html","code_str"]:
                dict_pd[key+"_rm_outlier"].append(dict_pd_remove_outlier[key][index])
    #'''
    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
    for i, e in enumerate(dict_pd['RCIW_rm_outlier']):
        if dict_pd['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_pd['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
        else:
            perf_change_zonghe_list.append(dict_pd['perf_change'][i])
            RCIW_zonghe_list.append(dict_pd['RCIW'][i])
    dict_pd["perf_change_zonghe"] = perf_change_zonghe_list
    dict_pd["RCIW_zonghe"] = RCIW_zonghe_list
    csv_feature_file_name_corr_dir=util.data_root_mv +"lab_performance/for_multi_targets_benchmarks/csv/"
    csv_feature_file_name_corr=csv_feature_file_name_corr_dir+"for_multi_targets_lab_performance_features.csv"
    # csv_feature_file_name_corr= util.data_root_mv + "lab_performance/call_star_benchmarks/csv/call_star_feature.csv"
    if not os.path.exists(csv_feature_file_name_corr_dir):
        os.makedirs(csv_feature_file_name_corr_dir)
    save_features_add_interval(dict_pd)
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

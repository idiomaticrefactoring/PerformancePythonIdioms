import time
import traceback

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy
import matplotlib.pyplot as plt
import subprocess
import pandas as pd

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
def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_perf_change = lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change)
    # dict_pd=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change_remove_outlier)

    # '''
    dict_pd_remove_outlier = lab_performance_util.get_ci_perf_change_dict(
        save_code_info_dir_add_performance_change_remove_outlier)
    for key in dict_pd_remove_outlier:
        if key not in ["file_html", "code_str"]:
            dict_perf_change[key + "_rm_outlier"] = []
    for file_html in dict_perf_change["file_html"]:
        index = dict_pd_remove_outlier["file_html"].index(file_html)
        for key in dict_pd_remove_outlier:
            if key not in ["file_html", "code_str"]:
                dict_perf_change[key + "_rm_outlier"].append(dict_pd_remove_outlier[key][index])
    # '''
    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
    perf_change_zonghe_left_list = []
    perf_change_zonghe_right_list = []
    for i, e in enumerate(dict_perf_change['RCIW_rm_outlier']):
        if dict_perf_change['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_perf_change['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
            perf_change_zonghe_left_list.append(dict_perf_change["perf_change_left_rm_outlier"][i])
            perf_change_zonghe_right_list.append(dict_perf_change["perf_change_right_rm_outlier"][i])

        else:
            perf_change_zonghe_list.append(dict_perf_change['perf_change'][i])
            RCIW_zonghe_list.append(dict_perf_change['RCIW'][i])
            perf_change_zonghe_left_list.append(dict_perf_change["perf_change_left"][i])
            perf_change_zonghe_right_list.append(dict_perf_change["perf_change_right"][i])

    dict_perf_change["perf_change_zonghe"] = perf_change_zonghe_list
    dict_perf_change["RCIW_zonghe"] = RCIW_zonghe_list
    dict_perf_change["perf_change_right_zonghe"] = perf_change_zonghe_right_list
    dict_perf_change["perf_change_left_zonghe"] = perf_change_zonghe_left_list

    dict_pd = {"file_html":[],"code_str":[],"RCIW":[],"perf_change_right":[],"perf_change_left":[],"perf_change":[],
               "num_assign_node":[],"is_const":[],"context":[],"is_swap":[]}#"kind":[],

    # '''
    # dict_pd["file_html"]=dict_perf_change["file_html"]
    # dict_pd["code_str"] = dict_perf_change["code_str"]
    for ind, file_name in enumerate(dict_perf_change["file_html"]):

        file_name_no_suffix = file_name[:-4]
        num_node_str = int(file_name.split("_")[0])
        if "_swap" in file_name:
            continue
        if "_const" in file_name:
            continue

        dict_pd["file_html"].append(dict_perf_change["file_html"][ind])
        dict_pd["code_str"].append( dict_perf_change["code_str"][ind])
        dict_pd["RCIW"].append(RCIW_zonghe_list[ind])
        dict_pd["perf_change_right"].append(perf_change_zonghe_right_list[ind])
        dict_pd["perf_change_left"].append(perf_change_zonghe_left_list[ind])
        dict_pd["perf_change"].append(perf_change_zonghe_list[ind])
        if "_swap" in file_name:
            dict_pd["is_swap"].append(1)
        else:
            dict_pd["is_swap"].append(0)
        dict_pd["num_assign_node"].append(num_node_str)

        if "_const" in file_name:
            dict_pd["is_const"].append(1)

        else:
            dict_pd["is_const"].append(0)


        if "_func" in file_name:
            dict_pd["context"].append(1)
        else:
            dict_pd["context"].append(0)
        # low = (dict_pd["perf_change_left"][ind])
        # e=dict_pd["perf_change_right"][ind]
        # if low <= 1 <= e:
        #
        #     dict_pd["kind"].append("unchange")
        # elif low > 1:
        #
        #     dict_pd["kind"].append("improve")
        # else:
        #
        #     dict_pd["kind"].append("regression")
    dataMain = pd.DataFrame(data=dict_pd)
    for key in dataMain:
        feature = dataMain[key]
        # average=feature.mean()
        # std = feature.std()
        try:
            a = scipy.stats.skew(feature)
            print("skew: ", key, a)
        except:
            print(f"the key {key} cannot compute the skew")
            traceback.print_exc()
    return dict_pd

def get_features_add_interval_no_swap(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_perf_change = lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change)
    # dict_pd=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change_remove_outlier)

    # '''
    dict_pd_remove_outlier = lab_performance_util.get_ci_perf_change_dict(
        save_code_info_dir_add_performance_change_remove_outlier)
    for key in dict_pd_remove_outlier:
        if key not in ["file_html", "code_str"]:
            dict_perf_change[key + "_rm_outlier"] = []
    for file_html in dict_perf_change["file_html"]:
        index = dict_pd_remove_outlier["file_html"].index(file_html)
        for key in dict_pd_remove_outlier:
            if key not in ["file_html", "code_str"]:
                dict_perf_change[key + "_rm_outlier"].append(dict_pd_remove_outlier[key][index])
    # '''
    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
    perf_change_zonghe_left_list = []
    perf_change_zonghe_right_list = []
    for i, e in enumerate(dict_perf_change['RCIW_rm_outlier']):
        if dict_perf_change['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_perf_change['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
            perf_change_zonghe_left_list.append(dict_perf_change["perf_change_left_rm_outlier"][i])
            perf_change_zonghe_right_list.append(dict_perf_change["perf_change_right_rm_outlier"][i])

        else:
            perf_change_zonghe_list.append(dict_perf_change['perf_change'][i])
            RCIW_zonghe_list.append(dict_perf_change['RCIW'][i])
            perf_change_zonghe_left_list.append(dict_perf_change["perf_change_left"][i])
            perf_change_zonghe_right_list.append(dict_perf_change["perf_change_right"][i])

    dict_perf_change["perf_change_zonghe"] = perf_change_zonghe_list
    dict_perf_change["RCIW_zonghe"] = RCIW_zonghe_list
    dict_perf_change["perf_change_right_zonghe"] = perf_change_zonghe_right_list
    dict_perf_change["perf_change_left_zonghe"] = perf_change_zonghe_left_list

    dict_pd = {"file_html":[],"code_str":[],"RCIW":[],"perf_change_right":[],"perf_change_left":[],"perf_change":[],
               "num_assign_node":[],"is_const":[],"context":[],"is_swap":[]}
    # dict_pd["file_html"] = dict_perf_change["file_html"]
    # dict_pd["code_str"] = dict_perf_change["code_str"]
    # dict_pd["RCIW"]=RCIW_zonghe_list
    # dict_pd["perf_change_right"]=perf_change_zonghe_right_list
    # dict_pd["perf_change_left"] = perf_change_zonghe_left_list
    # dict_pd["perf_change"] = perf_change_zonghe_list
    # '''
    # dict_pd["file_html"]=dict_perf_change["file_html"]
    # dict_pd["code_str"] = dict_perf_change["code_str"]
    for ind, file_name in enumerate(dict_perf_change["file_html"]):

        file_name_no_suffix = file_name[:-4]
        num_node_str = int(file_name.split("_")[0])
        if "_swap" in file_name:
            continue
        if "_const" in file_name:
            continue
        dict_pd["file_html"].append(dict_perf_change["file_html"][ind])
        dict_pd["code_str"].append(dict_perf_change["code_str"][ind])
        dict_pd["RCIW"].append(RCIW_zonghe_list[ind])
        dict_pd["perf_change_right"].append(perf_change_zonghe_right_list[ind])
        dict_pd["perf_change_left"].append(perf_change_zonghe_left_list[ind])
        dict_pd["perf_change"].append(perf_change_zonghe_list[ind])
        if "_swap" in file_name:
            dict_pd["is_swap"].append(1)
        else:
            dict_pd["is_swap"].append(0)
        dict_pd["num_assign_node"].append(num_node_str)

        if "_const" in file_name:
            dict_pd["is_const"].append(1)

        else:
            dict_pd["is_const"].append(0)


        if "_func" in file_name:
            dict_pd["context"].append(1)
        else:
            dict_pd["context"].append(0)
        # low = (dict_pd["perf_change_left"][ind])
        # e=dict_pd["perf_change_right"][ind]
        # if low <= 1 <= e:
        #
        #     dict_pd["kind"].append("unchange")
        # elif low > 1:
        #
        #     dict_pd["kind"].append("improve")
        # else:
        #
        #     dict_pd["kind"].append("regression")
    dataMain = pd.DataFrame(data=dict_pd)
    for key in dataMain:
        feature = dataMain[key]
        # average=feature.mean()
        # std = feature.std()
        try:
            a = scipy.stats.skew(feature)
            print("skew: ", key, a)
        except:
            print(f"the key {key} cannot compute the skew")
            traceback.print_exc()
    return dict_pd
def get_reason(dataMain):
    file_html=dataMain["file_html"]
    perf_change=dataMain["perf_change"]
    unique_num=0
    add_num=0
    remove_num=0
    for ind,file_name in enumerate(file_html):

        if  file_name.startswith("2_ass_swap") or  file_name.startswith("3_ass_swap"):
            print(file_name)
            unique_num+=1
        elif perf_change[ind]>1:
            remove_num+=1
        else:
            add_num+=1
    sum_num=unique_num+remove_num+add_num
    print(unique_num,remove_num,add_num)
    print(unique_num/sum_num, remove_num/sum_num, add_num/sum_num)


if __name__ == '__main__':
    # bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    # total_file_list = [e[:-3] for e in os.listdir(bench_dir)]

    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3_improve/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/multi_ass_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/multi_ass_benchmarks_30/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/multi_ass_benchmarks/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/multi_ass_benchmarks_30/prefined_cpus_remain_code_new_add_perf_change/50/"

    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    # dict_pd=get_features_add_interval_no_swap(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)

    csv_perf_change_dir= util.data_root + "lab_performance/multi_ass_benchmarks_30/csv/"

    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    csv_feature_file_name_corr= util.data_root + "lab_performance/multi_ass_benchmarks_30/csv/train_data_multi_ass.csv"
    csv_feature_file_name_corr= util.data_root + "lab_performance/multi_ass_benchmarks_30/csv/train_data_multi_ass_noswap_noconst.csv"

    # csv_feature_file_name_corr= util.data_root + "lab_performance/multi_ass_benchmarks_30/csv/train_data_multi_ass_no_swap.csv"

    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)

    df_sample=dataMain.sample(n=120,random_state=2022,ignore_index=True)
    df_sample.to_csv(csv_perf_change_dir + "sample_multi_ass.csv", index=False)
    get_reason(df_sample)
    '''
    dict_pd["kind"]=[]
    dict_pd_improve = {"num_ele": [], 'num_subscript': [],
                       "is_value_const": [], 'is_lower_0': [], 'is_upper_len': [],
                       'is_step_1': [], 'context': []}
    dict_pd_unchange = {"num_ele": [], 'num_subscript': [],
                        "is_value_const": [], 'is_lower_0': [], 'is_upper_len': [],
                        'is_step_1': [], 'context': []}
    dict_pd_decrease = {"num_ele": [], 'num_subscript': [],
                        "is_value_const": [], 'is_lower_0': [], 'is_upper_len': [],
                        'is_step_1': [], 'context': []}
    for ind, e in enumerate(dict_pd["perf_change_right"]):

        low = (dict_pd["perf_change_left"][ind])
        if low <= 1 <= e:
            for key in dict_pd_unchange:
                dict_pd_unchange[key].append(dict_pd[key][ind])
            dict_pd["kind"].append("unchange")
        elif low > 1:
            for key in dict_pd_unchange:
                dict_pd_improve[key].append(dict_pd[key][ind])
            dict_pd["kind"].append("improve")
        else:
            for key in dict_pd_unchange:
                dict_pd_decrease[key].append(dict_pd[key][ind])
            dict_pd["kind"].append("regression")
    print("unchange perf infor: ",len(dict_pd_unchange[list(dict_pd_unchange.keys())[0]]))
    '''

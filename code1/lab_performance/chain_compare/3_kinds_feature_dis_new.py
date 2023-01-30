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


    dict_pd = {"file_html":[], "code_str":[],"RCIW": [], "perf_change_right": [], "perf_change_left": [], "perf_change": [], "kind": [],
               'num_cmpop': [], "num_true": [],"is_true":[], "num_Lt": [], "num_Gt": [],
               "num_Eq": [], "num_NotEq": [], "num_LtE": [], "num_GtE": [], "num_NotIn": [], "num_In": [], "num_Is": [],
               "num_IsNot": [],"has_Lt": [], "has_Gt": [],
               "has_Eq": [], "has_NotEq": [], "has_LtE": [], "has_GtE": [], "has_NotIn": [], "has_In": [], "has_Is": [],
               "has_IsNot": [], 'context': []}
    dict_pd["file_html"] = dict_perf_change["file_html"]
    dict_pd["code_str"] = dict_perf_change["code_str"]
    dict_pd["RCIW"]=RCIW_zonghe_list
    dict_pd["perf_change_right"]=perf_change_zonghe_right_list
    dict_pd["perf_change_left"] = perf_change_zonghe_left_list
    dict_pd["perf_change"] = perf_change_zonghe_list
    # '''
    # dict_pd["file_html"]=dict_perf_change["file_html"]
    # dict_pd["code_str"] = dict_perf_change["code_str"]
    for ind, file_name in enumerate(dict_perf_change["file_html"]):
        print(file_name)
        file_name_no_suffix = file_name[:-3]

        num_false = int(file_name_no_suffix.split("_")[0])
        # dict_pd["num_false"].append(num_false)

        cmpop_list = file_name_no_suffix.split("_")[1:]

        if "func" in cmpop_list:
            num_cmpop = len(cmpop_list) - 1
            dict_pd["num_cmpop"].append(len(cmpop_list) - 1)
        else:
            num_cmpop = len(cmpop_list)
            dict_pd["num_cmpop"].append(len(cmpop_list))
        # if not num_false:
        #     dict_pd["num_true"].append(num_cmpop-num_false)
        # else:
        dict_pd["num_true"].append(num_false)
        # dict_pd["is_true"].append(1 if num_false else 0)
        dict_pd["is_true"].append(num_cmpop==num_false)

        cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        for cmpop in cmpop_list:
            if cmpop == "==":
                cmpop_1 += 1
            elif cmpop == "!=":
                cmpop_2 += 1
            elif cmpop == "<=":
                cmpop_3 += 1
            elif cmpop == ">=":
                cmpop_4 += 1
            elif cmpop == "<":
                cmpop_5 += 1
            elif cmpop == ">":
                cmpop_6 += 1
            elif cmpop == "not in":
                cmpop_7 += 1
            elif cmpop == "in":
                cmpop_8 += 1
            elif cmpop == "is":
                cmpop_9 += 1
            elif cmpop == "is not":
                cmpop_10 += 1

        dict_pd["num_Eq"].append(cmpop_1)
        dict_pd["num_NotEq"].append(cmpop_2)
        dict_pd["num_LtE"].append(cmpop_3)
        dict_pd["num_GtE"].append(cmpop_4)
        dict_pd["num_Lt"].append(cmpop_5)
        dict_pd["num_Gt"].append(cmpop_6)
        dict_pd["num_NotIn"].append(cmpop_7)
        dict_pd["num_In"].append(cmpop_8)
        dict_pd["num_Is"].append(cmpop_9)
        dict_pd["num_IsNot"].append(cmpop_10)
        dict_pd["has_Eq"].append(1 if cmpop_1>0 else 0)
        dict_pd["has_NotEq"].append(1 if cmpop_2>0 else 0)
        dict_pd["has_LtE"].append(1 if cmpop_3>0 else 0)
        dict_pd["has_GtE"].append(1 if cmpop_4>0 else 0)
        dict_pd["has_Lt"].append(1 if cmpop_5>0 else 0)
        dict_pd["has_Gt"].append(1 if cmpop_6>0 else 0)
        dict_pd["has_NotIn"].append(1 if cmpop_7>0 else 0)
        dict_pd["has_In"].append(1 if cmpop_8>0 else 0)
        dict_pd["has_Is"].append(1 if cmpop_9>0 else 0)
        dict_pd["has_IsNot"].append(1 if cmpop_10>0 else 0)
        print(num_false, len(cmpop_list), cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8,
              cmpop_9, cmpop_10)

        if "_func" in file_name:
            dict_pd["context"].append(0)
        else:
            dict_pd["context"].append(1)
        low = (dict_pd["perf_change_left"][ind])
        e=dict_pd["perf_change_right"][ind]
        if low <= 1 <= e:

            dict_pd["kind"].append("unchange")
        elif low > 1:

            dict_pd["kind"].append("improve")
        else:

            dict_pd["kind"].append("regression")
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
if __name__ == '__main__':
    # bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    # total_file_list = [e[:-3] for e in os.listdir(bench_dir)]

    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3_improve/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/chain_compare_benchmarks_new/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_2/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/chain_compare_benchmarks_new/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_2/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/prefined_cpus_remain_code_new_add_perf_change/50/"

    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    # csv_feature_file_name_corr= util.data_root_mv + "lab_performance/chain_compare_benchmarks_new/csv/train_data_chain_compare_new.csv"

    csv_perf_change_dir = util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/csv/"
    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_chain_compare_new_3.csv"

    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)


    df_sample = dataMain.sample(n=30, random_state=2022)
    df_sample.to_csv(csv_perf_change_dir + "sample_chain_compare.csv", index=False)

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





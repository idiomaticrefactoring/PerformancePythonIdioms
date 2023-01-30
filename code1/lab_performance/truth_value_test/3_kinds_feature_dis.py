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

    dict_pd = {"file_html":[], "code_str":[],"RCIW":[],"perf_change_right":[],"perf_change_left":[],"perf_change":[],"kind":[],
               "comp_op":[],'node_kind': [],"empty_kind":[],
              'context': []}
    # ,"is_None":[], "is_False":[], "is_0":[], "is_0.0":[], "is_0j":[], "is_Decimal(0)":[], "is_Fraction(0, 1)":[], "is_empty_string":[], "is_()":[], "is_[]":[], "is_{}":[],
    #                  "is_dict()":[], "is_set()":[], "is_range(0)":[]}
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

        file_name_no_suffix = file_name[:-4]
        # if file_name_no_suffix!="_empty_!=_equal_flag_while_node":
        #     continue
        empty = file_name_no_suffix.split("_")[0]
        dict_pd["empty_kind"].append(empty)



        # print("why not have the feature: ",dict_pd)

        if "==" in file_name:
            dict_pd["comp_op"].append("==")
        else:
            dict_pd["comp_op"].append("!=")

        # if "if_node" in file_name:
        #     dict_pd["node_kind"].append("if")
        # elif "while_node" in file_name:
        #     dict_pd["node_kind"].append("while")
        # else:
        #     dict_pd["node_kind"].append("assert")

        if "if_node" in file_name:
            dict_pd["node_kind"].append("if_node")
        elif "while_node" in file_name:
            dict_pd["node_kind"].append("while_node")
        else:
            dict_pd["node_kind"].append("assert_node")

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
    # print(dict_pd["kind"])
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
    # print(dict_pd["kind"])
    return dict_pd
if __name__ == '__main__':
    # bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    # total_file_list = [e[:-3] for e in os.listdir(bench_dir)]

    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3_improve/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"

    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    csv_feature_file_name_corr= util.data_root_mv + "lab_performance/truth_value_test_benchmarks/csv/rq2_data_truth_value_test.csv"
    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)


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

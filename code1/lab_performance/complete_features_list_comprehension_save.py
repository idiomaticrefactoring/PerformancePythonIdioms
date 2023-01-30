import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_list_comprehension
import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util,util_perf
from lab_code_info import LabCodeInfo

import pandas as pd
# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
import numpy as np

from math import log
import scipy as sp

from scipy import stats

from sklearn import preprocessing
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

#from sklearn.cross_validation import train_test_split

import statsmodels.formula.api as smf
import seaborn as sns

import warnings
def save_features():
        dict_pd = dict()
        # '''
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                print("file_name: ", file_name)
                file_name_no_suffix = file_name[:-4]
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: LabCodeInfo
                # print("code path: ",lab_code_info.file_path)
                # print("num_for, num_if, num_if_else, e_input: ",num_for, num_if, num_if_else, e_input)
                for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
                # print("code: ")
                # print(ast.unparse(for_node))
                # print(ast.unparse(assign_node))
                # print(remove_ass_flag)
                # print(ast.unparse(new_tree))
                new_node_list = [new_tree]
                if not remove_ass_flag:
                        new_node_list.append(assign_node)
                dict_features_old = util_perf.get_features([for_node, assign_node])  # .get_features()
                dict_features_new = util_perf.get_features(new_node_list)  # .get_features()
                dict_difference = {"num_ele": int(lab_code_info.num_add_ele)}
                # for key in dict_features_old:
                #         dict_difference[key+"_diff"]=dict_features_old[key]-dict_features_new[key]
                dict_features = {**dict_features_old, **dict_difference}
                # print(dict_features)
                # break

                mean_perf_change, left, right = lab_code_info.get_performance_info()
                for fea in dict_features:
                        ele = dict_features[fea]  # np.log(dict_features[fea])
                        if fea not in dict_pd:

                                dict_pd[fea] = [ele]
                        else:
                                dict_pd[fea].append(ele)
                if "perf_change" not in dict_pd:
                        dict_pd["perf_change"] = [mean_perf_change]
                else:
                        dict_pd["perf_change"].append(mean_perf_change)
                print("perf_change: ", file_name,mean_perf_change,left, right)
        util.save_pkl(feature_info_dir, feature_file_name, dict_pd)
        # util.save_pkl(feature_info_dir, feature_file_name, dict_pd)
def remove_features():
        dict_pd = util.load_pkl(feature_info_dir, feature_file_name)

        # dict_pd["perf_change"] = np.log(dict_pd["perf_change"])
        stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
        # warnings.filterwarnings(action='once')
        warnings.filterwarnings(action='default')
        # load Data
        dataMain = pd.DataFrame(data=dict_pd)
        dataMain.to_csv(csv_feature_file_name, index=False)


        same_feature_list = []
        for key in dataMain:
                if len(set(dataMain[key])) <= 1:
                        # print(key)
                        same_feature_list.append(key)
                        # dataMain.drop
        print("same_feature_list: ", same_feature_list)
        dataMain.drop(columns=same_feature_list,inplace=True)
        print(dataMain.columns)
        remove_feature_list = ['num_Delimiters','num_var','num_param']
        dataMain.drop(columns=remove_feature_list, inplace=True)
        print(dataMain.columns)
        dataMain.to_csv(csv_feature_file_name_corr, index=False)
        '''
        remove_feature_list = ["num_Delimiters_diff", "num_line_diff", "num_Delimiters", 'num_var', 'num_line',
                               "num_var_diff", "num_param_diff", "num_if_else_diff", "num_func_call_diff",
                               "num_func_call", "num_constant", "num_Keywords_diff", 'num_Attr_diff',
                               'num_param', 'num_Operators', "num_Attr", 'num_loop_diff', 'num_if_diff']  # []
        '''
        # feature_important=["num_Delimiters_diff",]
        remove_feature_list =["num_constant","num_Operators","num_line",'num_func_call','num_Keywords','num_Attr']
        dict_corr_num = dict()
        corr = dataMain.corr().to_dict()
        print(corr)
        for f1_name in corr:
                for e_another in corr[f1_name]:
                        if corr[f1_name][e_another] is pd.NA or corr[f1_name][e_another] > 0.7 or corr[f1_name][
                                e_another] < -0.7:

                                if f1_name in remove_feature_list or e_another in remove_feature_list:
                                        continue
                                if f1_name not in dict_corr_num:
                                        dict_corr_num[f1_name] = 0
                                dict_corr_num[f1_name] += 1
                                print(f1_name, e_another, corr[f1_name][e_another])
        remove_feature_list = ["num_func_call", "num_Attr", "num_param", "num_var", "num_loop_diff", "num_if_diff"]
        print("dict_corr_num: ", sorted(dict_corr_num.items(), key=lambda kv: (kv[1], kv[0])))
        # dict_corr_num:  [('num_Keywords', 1), ('num_ele', 1), ('num_if', 1), ('num_if_else', 1), ('num_loop', 1), ('perf_change', 1)]
def save_features_add_interval():
        dict_pd = dict()
        # '''
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                print("file_name: ", file_name)
                file_name_no_suffix = file_name[:-4]
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: LabCodeInfo
                # print("code path: ",lab_code_info.file_path)
                # print("num_for, num_if, num_if_else, e_input: ",num_for, num_if, num_if_else, e_input)
                for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
                # print("code: ")
                # print(ast.unparse(for_node))
                # print(ast.unparse(assign_node))
                # print(remove_ass_flag)
                # print(ast.unparse(new_tree))
                new_node_list = [new_tree]
                if not remove_ass_flag:
                        new_node_list.append(assign_node)
                dict_features_old = util_perf.get_features([for_node, assign_node])  # .get_features()
                dict_features_new = util_perf.get_features(new_node_list)  # .get_features()
                dict_difference = {"num_ele": int(lab_code_info.num_add_ele)}
                # for key in dict_features_old:
                #         dict_difference[key+"_diff"]=dict_features_old[key]-dict_features_new[key]
                dict_features = {**dict_difference,**dict_features_old, }
                # print(dict_features)
                # break

                mean_perf_change, left, right = lab_code_info.get_performance_info()
                if "perf_change" not in dict_pd:
                        dict_pd["perf_change"] = [mean_perf_change]
                else:
                        dict_pd["perf_change"].append(mean_perf_change)
                if "perf_change_left" not in dict_pd:
                        dict_pd["perf_change_left"] = [left]
                else:
                        dict_pd["perf_change_left"].append(left)
                if "perf_change_right" not in dict_pd:
                        dict_pd["perf_change_right"] = [right]
                else:
                        dict_pd["perf_change_right"].append(right)
                for fea in dict_features:
                        ele = dict_features[fea]  # np.log(dict_features[fea])
                        if fea not in dict_pd:

                                dict_pd[fea] = [ele]
                        else:
                                dict_pd[fea].append(ele)

                print("perf_change: ", file_name,mean_perf_change,left, right)
        dataMain = pd.DataFrame(data=dict_pd)
        # dataMain.to_csv(csv_feature_file_name_add_interval, index=False)
if __name__ == '__main__':

        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks/final_stable/"
        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_mod/prefined_cpus_remain_code/"
        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_10_7/prefined_cpus_remain_code/"
        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_10_7_add_func/prefined_cpus_remain_code/"
        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_10_7_add_func_test/prefined_cpus_remain_code/"
        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code/"

        feature_info_dir=util.data_root + "lab_performance/feature/list_compre_benchmarks/"
        feature_file_name="list_comprehension"
        feature_file_name="list_comprehension_original"
        feature_file_name="list_comprehension_original_complete_features"
        feature_file_name="list_compre_benchmarks_mod_complete_features"
        feature_file_name="list_compre_bench_complete_features_10_7"
        feature_file_name="list_compre_benchmarks_fun_and_Nfunc_features"

        csv_feature_file_name="labperformance_listcomprehension_complete_feature.csv"
        csv_feature_file_name="labperformance_listcomprehension_mod_complete_feature.csv"
        csv_feature_file_name="labperformance_list_compre_bench_complete_features_10_7.csv"
        csv_feature_file_name="list_compre_benchmarks_fun_and_Nfunc_features.csv"

        csv_feature_file_name_corr="labperformance_list_compre_bench_complete_features_10_7_corra.csv"
        csv_feature_file_name_corr="list_compre_benchmarks_fun_and_Nfunc_features_corr.csv"
        csv_feature_file_name_add_interval="labperformance_list_compre_bench_complete_features_10_7_corra_add_interval.csv"
        csv_feature_file_name_add_interval="list_compre_benchmarks_fun_and_Nfunc_features_corr_add_interval.csv"

        # save_features()
        # remove_features()
        save_features_add_interval()
        '''
        dict_pd = util.load_pkl(feature_info_dir, feature_file_name)

        # dict_pd["perf_change"] = np.log(dict_pd["perf_change"])
        stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
        # warnings.filterwarnings(action='once')
        warnings.filterwarnings(action='default')
        # load Data
        dataMain = pd.DataFrame(data=dict_pd)
        dataMain.to_csv(csv_feature_file_name, index=False)

        # print(corr)
        same_feature_list=[]
        for key in dataMain:
                if len(set(dataMain[key])) <= 1:
                        # print(key)
                        same_feature_list.append(key)
                        # dataMain.drop
        print("same_feature_list: ",same_feature_list)
        dataMain.drop(columns=same_feature_list)
        print(dataMain.columns)
        remove_feature_list = ["num_Delimiters_diff","num_line_diff","num_Delimiters",'num_var','num_line',
                               "num_var_diff","num_param_diff","num_if_else_diff","num_func_call_diff",
                               "num_func_call","num_constant","num_Keywords_diff",'num_Attr_diff',
                               'num_param','num_Operators',"num_Attr",'num_loop_diff','num_if_diff']#[]
                               

        # feature_important=["num_Delimiters_diff",]
        dict_corr_num=dict()
        corr = dataMain.corr().to_dict()
        for f1_name in corr:
                for e_another in corr[f1_name]:
                        if corr[f1_name][e_another] is pd.NA or corr[f1_name][e_another]>0.7 or corr[f1_name][e_another]<-0.7:

                                if f1_name in remove_feature_list or e_another in remove_feature_list:
                                        continue
                                if f1_name not in dict_corr_num:
                                        dict_corr_num[f1_name]=0
                                dict_corr_num[f1_name]+=1
                                print(f1_name,e_another,corr[f1_name][e_another])
        remove_feature_list=["num_func_call","num_Attr","num_param","num_var","num_loop_diff","num_if_diff"]
        print("dict_corr_num: ",sorted(dict_corr_num.items(), key = lambda kv:(kv[1], kv[0])))
        #dict_corr_num:  [('num_Keywords', 1), ('num_ele', 1), ('num_if', 1), ('num_if_else', 1), ('num_loop', 1), ('perf_change', 1)]
        '''
import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)

sys.path.append(code_dir+"wrap_refactoring/")
import util
import util_perf
from code_info import CodeInfo

import pandas as pd
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
        count_code=0
        count_instance=0
        count_test_me=0
        count_size_of_null=0
        # '''
        # 第9个data:  {'num_ele': [0, 2], 'perf_change': [1.5406070811248669, 0.950779229519387], 'num_loop': [1, 1], 'num_if': [1, 1], 'num_if_else': [0, 0], 'num_func_call': [2, 2], 'num_param': [2, 2], 'num_var': [7, 7], 'num_List': [1, 1], 'num_Dict': [0, 0], 'num_Set': [0, 0], 'num_Tuple': [0, 0], 'num_Subscript': [0, 0], 'num_Slice': [0, 0], 'num_Attr': [2, 2], 'num_constant': [1, 1], 'num_line': [4, 4], 'num_Keywords': [5, 5], 'num_Operators': [0, 0], 'num_Delimiters': [11, 11]}
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                print("file_name: ", ind,file_name)
                file_name_no_suffix = file_name[:-4]
                size_obj_dict = util.load_pkl(sizeof_code_info_dir, file_name_no_suffix)
                # print("size_obj_dict: ",size_obj_dict)
                # break
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: CodeInfo
                for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
                # print("total_time_list_info_dict: ",lab_code_info.total_time_list_info_dict)
                total_time_list_info_dict=lab_code_info.total_time_list_info_dict
                if not total_time_list_info_dict:
                        continue
                new_node_list = [new_tree]
                if not remove_ass_flag:
                        new_node_list.append(assign_node)
                dict_features = util_perf.get_features([for_node, assign_node])  # .get_features()

                # print("features: ", ast.unparse(for_node), "\n", ast.unparse(assign_node))
                # print("features: ", dict_features)
                one_code_num_list=[]
                for test_me in total_time_list_info_dict:
                        count_test_me+=1
                        for instance in total_time_list_info_dict[test_me]:
                                instance_feature=total_time_list_info_dict[test_me][instance]
                                if test_me not in size_obj_dict or instance not in size_obj_dict[test_me]:
                                        count_size_of_null+=1
                                        continue
                                if "size_obj" not in dict_pd:
                                        dict_pd["size_obj"] = [int(size_obj_dict[test_me][instance][0])]
                                else:
                                        dict_pd["size_obj"].append(int(size_obj_dict[test_me][instance][0]))
                                if "num_ele" not in dict_pd:
                                        dict_pd["num_ele"] = [instance_feature['num_ele']]
                                else:
                                        dict_pd["num_ele"].append(instance_feature['num_ele'])
                                one_code_num_list.append([instance_feature['num_ele'],int(size_obj_dict[test_me][instance][0]),instance_feature['perf_change'][0]])

                                if 'perf_change' not in dict_pd:
                                        dict_pd['perf_change'] = [instance_feature['perf_change'][0]]
                                else:
                                        dict_pd['perf_change'].append(instance_feature['perf_change'][0])
                                for fea in dict_features:
                                        ele = dict_features[fea]  # np.log(dict_features[fea])
                                        if fea not in dict_pd:

                                                dict_pd[fea] = [ele]
                                        else:
                                                dict_pd[fea].append(ele)
                                count_instance+=1
                count_code+=1
                print("one_code_num_list: ",one_code_num_list,count_size_of_null)

        util.save_pkl(feature_info_dir, feature_file_name, dict_pd)
        print("count: ",count_code,count_test_me,count_instance)
def remove_features():
        dict_pd = util.load_pkl(feature_info_dir, feature_file_name)

        # dict_pd["perf_change"] = np.log(dict_pd["perf_change"])
        stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
        # warnings.filterwarnings(action='once')
        warnings.filterwarnings(action='default')
        # load Data
        dataMain = pd.DataFrame(data=dict_pd)
        print(dataMain.to_dict())
        dataMain.to_csv(csv_feature_file_name, index=False)


        same_feature_list = []
        for key in dataMain:
                if len(set(dataMain[key])) <= 1:
                        # print(key)
                        same_feature_list.append(key)
                        # dataMain.drop
        print("same_feature_list: ", same_feature_list)
        dataMain.drop(columns=same_feature_list,inplace=True)
        print("all columns: ",dataMain.columns)
        remove_feature_list =['num_Delimiters','num_var','num_param','num_ele']
        dataMain.drop(columns=remove_feature_list, inplace=True)
        print("all columns without same value in one column: ",dataMain.columns)
        dataMain.to_csv(csv_feature_file_name_corr, index=False)
        '''
        remove_feature_list = ["num_Delimiters_diff", "num_line_diff", "num_Delimiters", 'num_var', 'num_line',
                               "num_var_diff", "num_param_diff", "num_if_else_diff", "num_func_call_diff",
                               "num_func_call", "num_constant", "num_Keywords_diff", 'num_Attr_diff',
                               'num_param', 'num_Operators', "num_Attr", 'num_loop_diff', 'num_if_diff']  # []
        '''
        # feature_important=["num_Delimiters_diff",]
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
def all_data_save():
        feature = pd.read_csv(csv_feature_file_name_corr)
        key_list=feature.columns.tolist()
        # print(key_list)
        dict_pd=dict()
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                # break
                print("file_name: ", ind,file_name)
                file_name_no_suffix = file_name[:-4]
                size_obj_dict = util.load_pkl(sizeof_code_info_dir, file_name_no_suffix)
                # print("size_obj_dict: ",size_obj_dict)
                # break
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: CodeInfo
                for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
                total_time_list_info_dict = lab_code_info.total_time_list_info_dict
                if not total_time_list_info_dict:
                        continue
                new_node_list = [new_tree]
                if not remove_ass_flag:
                        new_node_list.append(assign_node)
                dict_features = util_perf.get_features([for_node, assign_node])  # .get_features()

                # print("features: ", ast.unparse(for_node), "\n", ast.unparse(assign_node))
                # print("features: ", dict_features)
                one_code_num_list=[]
                for test_me in total_time_list_info_dict:
                        for instance in total_time_list_info_dict[test_me]:
                                instance_feature=total_time_list_info_dict[test_me][instance]
                                if test_me not in size_obj_dict or instance not in size_obj_dict[test_me]:
                                        continue
                                if "file_html" not in dict_pd:
                                        dict_pd["file_html"] = [lab_code_info.file_html]
                                else:
                                        dict_pd["file_html"].append(lab_code_info.file_html)
                                if "test_me_inf" not in dict_pd:
                                        dict_pd["test_me_inf"] = [str(test_me)+str(instance)]
                                else:
                                        dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                                if "size_obj" not in dict_pd:
                                        dict_pd["size_obj"] = [int(size_obj_dict[test_me][instance][0])]
                                else:
                                        dict_pd["size_obj"].append(int(size_obj_dict[test_me][instance][0]))
                                if "num_ele" not in dict_pd:
                                        dict_pd["num_ele"] = [instance_feature['num_ele']]
                                else:
                                        dict_pd["num_ele"].append(instance_feature['num_ele'])
                                one_code_num_list.append([instance_feature['num_ele'],int(size_obj_dict[test_me][instance][0]),instance_feature['perf_change'][0]])

                                if 'perf_change' not in dict_pd:
                                        dict_pd['perf_change'] = [instance_feature['perf_change']]#instance_feature['perf_change'][0]
                                else:
                                        dict_pd['perf_change'].append(instance_feature['perf_change'])#instance_feature['perf_change'][0]
                                for fea in dict_features:
                                        if fea not in key_list:
                                                continue
                                        ele = dict_features[fea]  # np.log(dict_features[fea])
                                        if fea not in dict_pd:

                                                dict_pd[fea] = [ele]
                                        else:
                                                dict_pd[fea].append(ele)

        dataMain = pd.DataFrame(data=dict_pd)
        # print(dataMain.to_dict())
        dataMain.to_csv("all_feature_list_comprehension.csv", index=False)




if __name__ == '__main__':

        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks/final_stable/"
        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_mod/prefined_cpus_remain_code/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_perf_change/"
        feature_info_dir=util.data_root + "lab_performance/feature/list_compre_benchmarks/"
        feature_file_name="list_comprehension"
        feature_file_name="list_comprehension_original"
        feature_file_name="list_comprehension_original_complete_features"
        feature_file_name="list_compre_benchmarks_complete_features"
        feature_file_name="list_compre_benchmarks_complete_features_add_sizeof"
        feature_file_name="list_compre_benchmarks_complete_features_add_FanIn_Call_ExpVar"
        csv_feature_file_name="labperformance_listcomprehension_complete_feature.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_FanIn_Call_ExpVar.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_corr.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_FanIn_Call_ExpVar_corr.csv"
        # csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr.csv"
        #'''
        sizeof_code_info_dir = util.data_root + "performance/list_compre_benchmarks_sizeof_feature/"
        dynamic_code_info_dir = util.data_root + "performance/list_compre_benchmarks_sizeof_type_num_ele_feature/"

        # save_features()
        # remove_features()
        all_data_save()
        data=pd.read_csv(csv_feature_file_name_corr).to_dict()
        print(list(data.keys()))

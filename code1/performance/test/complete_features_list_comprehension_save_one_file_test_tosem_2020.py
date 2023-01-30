import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")

sys.path.append(code_dir+"wrap_refactoring/")
import util
import util_perf
from code_info import CodeInfo
from scipy.stats import ranksums, mannwhitneyu
import cliffsDelta
import pandas as pd
import numpy as np

from math import log
import scipy as sp
import re
from scipy import stats

from sklearn import preprocessing
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

#from sklearn.cross_validation import train_test_split

import statsmodels.formula.api as smf
import seaborn as sns

import warnings
def get_var_fea(dict_pd,one_instance_var_dict,real_var_info):
        if "Var" not in dict_pd:
                dict_pd['Var'] = []
        if "expVar" not in dict_pd:
                dict_pd['expVar'] = []
        if "FanIn" not in dict_pd:
                dict_pd['FanIn'] = []
        if "externalCall" not in dict_pd:
                dict_pd['externalCall'] = []
        if "expVar_unique" not in dict_pd:
                dict_pd['expVar_unique'] = []
        if "FanIn_unique" not in dict_pd:
                dict_pd['FanIn_unique'] = []
        if "externalCall_unique" not in dict_pd:
                dict_pd['externalCall_unique'] = []
        if "expVar_list" not in dict_pd:
                dict_pd['expVar_list'] = []
        if "FanIn_list" not in dict_pd:
                dict_pd['FanIn_list'] = []
        if "externalCall_list" not in dict_pd:
                dict_pd['externalCall_list'] = []
        expVar_list, FanIn_list, externalCall_list,Var_list= [], [], [], []
        num_expVar, num_FanIn, num_externalCall, num_Var = 0, 0, 0, 0
        for key in one_instance_var_dict:
                # print("value: ", key,one_instance_var_dict[key])
                pattern = re.compile("'(.*)'")
                var_type = pattern.findall(one_instance_var_dict[key])[0]
                # print("str: ", var_type)

                if var_type not in util_perf.builtins_types and "builtin" not in var_type and "method" not in var_type and "function" not in var_type and "NoneType" not in var_type and "module" not in var_type:
                        num_expVar += 1
                        expVar_list.append([key, var_type])
                if ('method' in var_type or "function" in var_type) and (
                        "builtin_function" not in var_type and ".append" not in key):
                        num_FanIn += 1
                        FanIn_list.append([key, var_type])
                if 'method' == var_type or 'function' == var_type:
                        num_externalCall += 1
                        externalCall_list.append([key, var_type])
        dict_pd['expVar_list'].append(expVar_list)
        dict_pd['FanIn_list'].append(FanIn_list)
        dict_pd['externalCall_list'].append(externalCall_list)
        dict_pd['expVar'].append(num_expVar)
        dict_pd['FanIn'].append(num_FanIn)
        dict_pd['externalCall'].append(num_externalCall)
def get_FanIn_ExCall_Var_ExpVar(dict_pd,one_instance_var_dict,for_node):
        for_code_str = ast.unparse(for_node)
        real_vars = []
        util.visit_vars_real(for_node, real_vars)
        func_call_list = []
        util.visit_func_call_real(for_node, func_call_list)
        if "expVar_unique" not in dict_pd:
                dict_pd['expVar_unique'] = []
        if "Var" not in dict_pd:
                dict_pd['Var'] = []
        if "expVar" not in dict_pd:
                dict_pd['expVar'] = []
        if "FanIn" not in dict_pd:
                dict_pd['FanIn'] = []
        if "externalCall" not in dict_pd:
                dict_pd['externalCall'] = []
        if "expVar_list" not in dict_pd:
                dict_pd['expVar_list'] = []
        if "Var_list" not in dict_pd:
                dict_pd['Var_list'] = []
        if "FanIn_list" not in dict_pd:
                dict_pd['FanIn_list'] = []
        if "externalCall_list" not in dict_pd:
                dict_pd['externalCall_list'] = []
        if "expVar_unique_list" not in dict_pd:
                dict_pd['expVar_unique_list'] = []
        expVar_unique_list, expVar_list, FanIn_list, externalCall_list, Var_list = [], [], [], [], []
        num_expVar, num_FanIn, num_externalCall, num_expVar_unique, num_Var = 0, 0, 0, 0, 0
        print("real_vars: ", real_vars, "  ------  ", list(one_instance_var_dict.keys()), "  ------  ",
              ast.unparse(for_node))
        totalVars = set([])
        for key in one_instance_var_dict:
                # print("value: ", key,one_instance_var_dict[key])
                pattern = re.compile("'(.*)'")
                var_type = pattern.findall(one_instance_var_dict[key])[0]
                # print("str: ", var_type)
                totalVars.add((key, var_type))
                if key in real_vars:
                        num_Var += 1
                        Var_list.append([key, var_type])
                # or 'type'!=var_type) and "builtin" not in var_type and "method" not in var_type and "function" not in var_type and "NoneType" not in var_type  and "module" not in var_type
                if var_type not in util_perf.builtins_types and key + '(' not in for_code_str:
                        num_expVar += 1
                        expVar_list.append([key, var_type])
                if key + '(' in for_code_str:  # and ("builtin_function" not in var_type and ".append" not in key):
                        num_FanIn += 1
                        FanIn_list.append([key, var_type])
                if key + '(' in for_code_str and key not in util.built_in:
                        num_externalCall += 1
                        externalCall_list.append([key, var_type])
                # if key in real_vars and var_type not in util_perf.builtins_types and "builtin" not in var_type and "method" not in var_type and "function" not in var_type and "NoneType" not in var_type:
                if key in real_vars and key + '(' not in for_code_str and var_type not in util_perf.builtins_types:
                        num_expVar_unique += 1
                        expVar_unique_list.append([key, var_type])
        # print("num: ",num_expVar,num_Var,num_expVar_unique,FanIn_list,num_FanIn,externalCall_list,num_externalCall)
        dict_pd['expVar_unique_list'].append(expVar_unique_list)
        dict_pd['expVar_list'].append(expVar_list)
        dict_pd['Var_list'].append(Var_list)
        dict_pd['FanIn_list'].append(FanIn_list)
        dict_pd['externalCall_list'].append(externalCall_list)
        dict_pd['expVar'].append(num_expVar)
        dict_pd['Var'].append(num_Var)
        if 'TotalVar' not in dict_pd:
                dict_pd['TotalVar'] = []
        dict_pd['TotalVar'].append(len(set(totalVars)))
        dict_pd['expVar_unique'].append(num_expVar_unique)
        dict_pd['FanIn'].append(num_FanIn)
        dict_pd['externalCall'].append(num_externalCall)
def get_FanIn_ExCall_Var_ExpVar_ast(dict_pd,one_instance_var_dict,for_node):
        real_vars = []
        util.visit_vars_real(for_node, real_vars)
        func_call_list = []
        util.visit_func_call_real(for_node, func_call_list)
        # if "expVar_unique" not in dict_pd:
        #         dict_pd['expVar_unique'] = []
        if "Var" not in dict_pd:
                dict_pd['Var'] = []
        if "expVar" not in dict_pd:
                dict_pd['expVar'] = []
        if "FanIn" not in dict_pd:
                dict_pd['FanIn'] = []
        if "externalCall" not in dict_pd:
                dict_pd['externalCall'] = []
        if "expVar_list" not in dict_pd:
                dict_pd['expVar_list'] = []
        if "Var_list" not in dict_pd:
                dict_pd['Var_list'] = []
        if "FanIn_list" not in dict_pd:
                dict_pd['FanIn_list'] = []
        if "externalCall_list" not in dict_pd:
                dict_pd['externalCall_list'] = []
        # if "expVar_unique_list" not in dict_pd:
        #         dict_pd['expVar_unique_list'] = []
        expVar_unique_list, expVar_list, FanIn_list, externalCall_list, Var_list = [], [], [], [], []
        num_expVar, num_FanIn, num_externalCall, num_expVar_unique, num_Var = 0, 0, 0, 0, 0
        # print("real_vars: ", real_vars, "  ------  ", list(one_instance_var_dict.keys()), "  ------  ",
        #       ast.unparse(for_node))
        totalVars = []
        for key in one_instance_var_dict:
                # print("value: ", key,one_instance_var_dict[key])
                pattern = re.compile("'(.*)'")
                var_type = pattern.findall(one_instance_var_dict[key])[0]
                # print("str: ", var_type)
                totalVars.append([key, var_type])
                if key in real_vars:
                        num_Var += 1
                        Var_list.append([key, var_type])
                # or 'type'!=var_type) and "builtin" not in var_type and "method" not in var_type and "function" not in var_type and "NoneType" not in var_type  and "module" not in var_type
                if key in real_vars and var_type not in util_perf.builtins_types and var_type not in ["module","NoneType"]:
                        num_expVar += 1
                        expVar_list.append([key, var_type])
                if key in func_call_list:  # and ("builtin_function" not in var_type and ".append" not in key):
                        num_FanIn += 1
                        FanIn_list.append([key, var_type])
                if key in func_call_list and key not in util.built_in and "builtin" not in var_type:
                        num_externalCall += 1
                        externalCall_list.append([key, var_type])
                # if key in real_vars and var_type not in util_perf.builtins_types and "builtin" not in var_type and "method" not in var_type and "function" not in var_type and "NoneType" not in var_type:
                # if key in real_vars and var_type not in util_perf.builtins_types:
                #         num_expVar_unique += 1
                #         expVar_unique_list.append([key, var_type])
        # print("num: ",num_expVar,num_Var,num_expVar_unique,FanIn_list,num_FanIn,externalCall_list,num_externalCall)
        # dict_pd['expVar_unique_list'].append(expVar_unique_list)
        dict_pd['expVar_list'].append(expVar_list)
        dict_pd['Var_list'].append(Var_list)
        dict_pd['FanIn_list'].append(FanIn_list)
        dict_pd['externalCall_list'].append(externalCall_list)
        dict_pd['expVar'].append(num_expVar)
        dict_pd['Var'].append(num_Var)
        if 'TotalVar' not in dict_pd:
                dict_pd['TotalVar'] = []
        dict_pd['TotalVar'].append(len(totalVars))
        # dict_pd['expVar_unique'].append(num_expVar_unique)
        dict_pd['FanIn'].append(num_FanIn)
        dict_pd['externalCall'].append(num_externalCall)

def save_features():
        # print("come here")
        perf_change_list=[]
        dict_pd = dict()
        file_code=0
        count_code=0
        count_instance=0
        count_test_me=0
        count_size_of_null=0
        count_var_null=0
        count_time_null=0

        # '''
        # 第9个data:  {'num_ele': [0, 2], 'perf_change': [1.5406070811248669, 0.950779229519387], 'num_loop': [1, 1], 'num_if': [1, 1], 'num_if_else': [0, 0], 'num_func_call': [2, 2], 'num_param': [2, 2], 'num_var': [7, 7], 'num_List': [1, 1], 'num_Dict': [0, 0], 'num_Set': [0, 0], 'num_Tuple': [0, 0], 'num_Subscript': [0, 0], 'num_Slice': [0, 0], 'num_Attr': [2, 2], 'num_constant': [1, 1], 'num_line': [4, 4], 'num_Keywords': [5, 5], 'num_Operators': [0, 0], 'num_Delimiters': [11, 11]}
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                file_code+=1
                one_code_num_list = []

                file_name_no_suffix = file_name[:-4]
                # size_obj_dict = util.load_pkl(sizeof_code_info_dir, file_name_no_suffix)
                dynamic_info_dict = util.load_pkl(dynamic_code_info_dir, file_name_no_suffix)

                # print("size_obj_dict: ",size_obj_dict)
                # break
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: CodeInfo
                for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info

                file_html = lab_code_info.file_html
                if file_html != "https://github.com/HunterMcGushion/hyperparameter_hunter/tree/master/hyperparameter_hunter/space/space_core.py":  # "https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv.py":
                        continue
                # if lab_code_info.file_html!="https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv_s.py":#"https://github.com/tanghaibao/goatools/tree/master/goatools/nt_utils.py":#"https://github.com/more-itertools/more-itertools/tree/master/more_itertools/more.py":#"https://github.com/networkx/networkx/tree/master/networkx/readwrite/json_graph/adjacency.py":#
                #         continue
                # stable_info_dict = lab_code_info.get_stable_info_dict()
                # total_time_list_info_dict = lab_code_info.get_stable_time_list(stable_info_dict=stable_info_dict)
                # print("total_time_list_info_dict: ",total_time_list_info_dict)
                # lab_code_info.get_performance_info(total_time_list_info_dict=total_time_list_info_dict)
                # print("total_time_list_info_dict: ",lab_code_info.total_time_list_info_dict)
                total_time_list_info_dict=lab_code_info.total_time_list_info_dict
                if not total_time_list_info_dict:
                        count_time_null+=1
                        print(">>>>time is none ",file_name,lab_code_info.file_html)
                        continue
                new_node_list = [new_tree]
                if not remove_ass_flag:
                        new_node_list.append(assign_node)
                dict_features = util_perf.get_features([for_node, assign_node])  # .get_features()
                size_obj_dict = dynamic_info_dict['size']
                vars_info_dict = dynamic_info_dict['var']
                # print("file_name: ", ind, file_name,lab_code_info.file_html)
                # print("vars_info_dict: ", vars_info_dict)
                for test_me in total_time_list_info_dict:
                        count_test_me += 1
                        for instance in total_time_list_info_dict[test_me]:
                                # total_time_list_info_dict = lab_code_info.get_stable_time_list(
                                #         stable_info_dict=stable_info_dict)
                                # # print("total_time_list_info_dict: ",total_time_list_info_dict)
                                instance_feature = total_time_list_info_dict[test_me][instance]
                                # print("instance_feature: ",instance_feature)
                                if test_me not in vars_info_dict or instance not in vars_info_dict[test_me]:
                                        print("*****************var is none: ",lab_code_info.file_html)
                                        count_var_null += 1
                                        continue
                                if test_me not in size_obj_dict or instance not in size_obj_dict[test_me]:
                                        count_size_of_null+=1
                                        continue
                                one_instance_var_dict = vars_info_dict[test_me][instance]
                                if "file_html" not in dict_pd:
                                        dict_pd["file_html"] = [lab_code_info.file_html]
                                else:
                                        dict_pd["file_html"].append(lab_code_info.file_html)
                                if "test_me_inf" not in dict_pd:
                                        dict_pd["test_me_inf"] = [str(test_me)+str(instance)]
                                else:
                                        dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                                if "code_str" not in dict_pd:
                                        dict_pd['code_str'] = [lab_code_info.get_code_str()]
                                else:
                                        dict_pd['code_str'].append(lab_code_info.get_code_str())
                                perf_change_list.append(instance_feature['perf_change'][0])
                                if 'perf_change' not in dict_pd:
                                        dict_pd['perf_change'] = [instance_feature['perf_change'][0]]
                                else:
                                        dict_pd['perf_change'].append(instance_feature['perf_change'][0])
                                if 'perf_change_left' not in dict_pd:
                                        dict_pd['perf_change_left'] = [instance_feature['perf_change'][1]]
                                else:
                                        dict_pd['perf_change_left'].append(instance_feature['perf_change'][1])
                                if 'perf_change_right' not in dict_pd:
                                        dict_pd['perf_change_right'] = [instance_feature['perf_change'][2]]
                                else:
                                        dict_pd['perf_change_right'].append(instance_feature['perf_change'][2])

                                if "size_obj" not in dict_pd:
                                        dict_pd["size_obj"] = [int(size_obj_dict[test_me][instance][0])]
                                else:
                                        dict_pd["size_obj"].append(int(size_obj_dict[test_me][instance][0]))
                                if "num_ele" not in dict_pd:
                                        dict_pd["num_ele"] = [instance_feature['num_ele']]
                                else:
                                        dict_pd["num_ele"].append(instance_feature['num_ele'])
                                # get_FanIn_ExCall_Var_ExpVar(dict_pd,one_instance_var_dict,for_node)
                                get_FanIn_ExCall_Var_ExpVar_ast(dict_pd,one_instance_var_dict,for_node)
                                one_code_num_list.append(
                                        [instance_feature['num_ele'], int(size_obj_dict[test_me][instance][0]),
                                         instance_feature['perf_change'][0]])

                                for fea in dict_features:
                                        ele = dict_features[fea]  # np.log(dict_features[fea])
                                        if fea not in dict_pd:
                                                dict_pd[fea] = [ele]
                                        else:
                                                dict_pd[fea].append(ele)
                                count_instance += 1
                count_code += 1
                # print("one_code_num_list: ",one_code_num_list,count_size_of_null)
        print(">>>>>>>>features: ",dict_pd.keys())
        dataMain = pd.DataFrame(data=dict_pd)
        print(">>>>>>drop same features: ", dataMain.keys())
        # print(dataMain.to_dict())
        dataMain.to_csv(csv_feature_file_name_useful, index=False)
        # print("perf_change_list: ",perf_change_list)
        a=[]
        loop_num=len(perf_change_list)//10
        print("loop_num: ",loop_num)
        for i in range(loop_num):

                a.append(perf_change_list[i*10:(i+1)*10])
                for ind_instance,e in enumerate(perf_change_list[i*10:(i+1)*10]):
                        print(e)
                        if e>1:
                                # print(i, ind_instance,e, dict_pd["expVar_list"][i*10+ind_instance],dict_pd["Var_list"][i*10+ind_instance])
                                pass


        print(a)
        print(f"median {np.median(perf_change_list)}, min {np.min(perf_change_list)}, "
              f"max {np.max(perf_change_list)}, average {np.mean(perf_change_list)}, std {np.std(perf_change_list)}: ",)
        # dataMain = drop_rows_same(dataMain)
        # dataMain.to_csv(csv_feature_file_name_no_same, index=False)
        #"expVar_unique_list",
        dataMain.drop(columns=[ "expVar_list","Var_list", "FanIn_list", "externalCall_list"], inplace=True)
        # util.save_pkl(feature_info_dir, feature_file_name, dataMain.to_dict())
        # dataMain.to_csv(csv_feature_file_name, index=False)
        # dataMain = drop_rows_same(dataMain)



        print("count: ",file_code,count_code,count_test_me,count_instance,count_var_null,count_size_of_null,count_time_null)
def save_perf_change(bench_time_info_dir,file_name_list=[]):
        print("len of code: ",len(os.listdir(bench_time_info_dir)))
        file_html_list = []
        num_ele_list=[]
        perf_change_list = []
        perf_left_change_list = []
        perf_right_change_list = []
        conf_inter_list = []
        file_code = 0
        count_code = 0
        count_instance = 0
        count_test_me = 0
        count_time_null = 0

        # '''
        # 第9个data:  {'num_ele': [0, 2], 'perf_change': [1.5406070811248669, 0.950779229519387], 'num_loop': [1, 1], 'num_if': [1, 1], 'num_if_else': [0, 0], 'num_func_call': [2, 2], 'num_param': [2, 2], 'num_var': [7, 7], 'num_List': [1, 1], 'num_Dict': [0, 0], 'num_Set': [0, 0], 'num_Tuple': [0, 0], 'num_Subscript': [0, 0], 'num_Slice': [0, 0], 'num_Attr': [2, 2], 'num_constant': [1, 1], 'num_line': [4, 4], 'num_Keywords': [5, 5], 'num_Operators': [0, 0], 'num_Delimiters': [11, 11]}
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
            if file_name not in file_name_list:
                continue
            file_code += 1
            file_name_no_suffix = file_name[:-4]
            lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
            lab_code_info: CodeInfo
            for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info

            file_html = lab_code_info.file_html
            if file_html != "https://github.com/HunterMcGushion/hyperparameter_hunter/tree/master/hyperparameter_hunter/space/space_core.py":  # "https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv.py":
                    continue
            total_time_list_info_dict = lab_code_info.total_time_list_info_dict
            if not total_time_list_info_dict:
                count_time_null += 1
                # print(">>>>time is none ", file_name, lab_code_info.file_html)
                continue
            new_node_list = [new_tree]
            if not remove_ass_flag:
                new_node_list.append(assign_node)
            # print("file_name: ", ind, file_name,lab_code_info.file_html)
            for test_me in total_time_list_info_dict:
                count_test_me += 1
                for instance in total_time_list_info_dict[test_me]:
                    instance_feature = total_time_list_info_dict[test_me][instance]
                    file_html_list.append(file_html)
                    num_ele_list.append(instance_feature['num_ele'])
                    perf_change_list.append(instance_feature['perf_change'][0])
                    perf_left_change_list.append(instance_feature['perf_change'][1])
                    perf_right_change_list.append(instance_feature['perf_change'][2])
                    conf_inter_list.append(instance_feature['perf_change'][2] - instance_feature['perf_change'][1])

                    count_instance += 1
            count_code += 1
        print("one_code_num_list: ",count_code,count_time_null,count_instance)
        return file_html_list,num_ele_list,perf_change_list, perf_left_change_list, perf_right_change_list, conf_inter_list

def save_features_tosem_2020():
        # print("come here")
        perf_change_list=[]
        dict_pd = dict()
        file_code=0
        count_code=0
        count_instance=0
        count_test_me=0
        count_size_of_null=0
        count_var_null=0
        count_time_null=0

        # '''
        # 第9个data:  {'num_ele': [0, 2], 'perf_change': [1.5406070811248669, 0.950779229519387], 'num_loop': [1, 1], 'num_if': [1, 1], 'num_if_else': [0, 0], 'num_func_call': [2, 2], 'num_param': [2, 2], 'num_var': [7, 7], 'num_List': [1, 1], 'num_Dict': [0, 0], 'num_Set': [0, 0], 'num_Tuple': [0, 0], 'num_Subscript': [0, 0], 'num_Slice': [0, 0], 'num_Attr': [2, 2], 'num_constant': [1, 1], 'num_line': [4, 4], 'num_Keywords': [5, 5], 'num_Operators': [0, 0], 'num_Delimiters': [11, 11]}
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                file_code+=1
                one_code_num_list = []

                file_name_no_suffix = file_name[:-4]
                # size_obj_dict = util.load_pkl(sizeof_code_info_dir, file_name_no_suffix)
                dynamic_info_dict = util.load_pkl(dynamic_code_info_dir, file_name_no_suffix)

                # print("size_obj_dict: ",size_obj_dict)
                # break
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: CodeInfo
                for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info

                file_html = lab_code_info.file_html
                if file_html != "https://github.com/HunterMcGushion/hyperparameter_hunter/tree/master/hyperparameter_hunter/space/space_core.py":  # "https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv.py":
                        continue
                # if lab_code_info.file_html!="https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv_s.py":#"https://github.com/tanghaibao/goatools/tree/master/goatools/nt_utils.py":#"https://github.com/more-itertools/more-itertools/tree/master/more_itertools/more.py":#"https://github.com/networkx/networkx/tree/master/networkx/readwrite/json_graph/adjacency.py":#
                #         continue
                # stable_info_dict = lab_code_info.get_stable_info_dict()
                # total_time_list_info_dict = lab_code_info.get_stable_time_list(stable_info_dict=stable_info_dict)
                # print("total_time_list_info_dict: ",total_time_list_info_dict)
                # lab_code_info.get_performance_info(total_time_list_info_dict=total_time_list_info_dict)
                # print("total_time_list_info_dict: ",lab_code_info.total_time_list_info_dict)
                total_time_list_info_dict=lab_code_info.total_time_list_info_dict
                if not total_time_list_info_dict:
                        count_time_null+=1
                        print(">>>>time is none ",file_name,lab_code_info.file_html)
                        continue
                new_node_list = [new_tree]
                if not remove_ass_flag:
                        new_node_list.append(assign_node)
                dict_features = util_perf.get_features([for_node, assign_node])  # .get_features()
                size_obj_dict = dynamic_info_dict['size']
                vars_info_dict = dynamic_info_dict['var']
                # print("file_name: ", ind, file_name,lab_code_info.file_html)
                # print("vars_info_dict: ", vars_info_dict)
                for test_me in total_time_list_info_dict:
                        count_test_me += 1
                        for instance in total_time_list_info_dict[test_me]:
                                # total_time_list_info_dict = lab_code_info.get_stable_time_list(
                                #         stable_info_dict=stable_info_dict)
                                # # print("total_time_list_info_dict: ",total_time_list_info_dict)
                                instance_feature = total_time_list_info_dict[test_me][instance]
                                # print("instance_feature: ",instance_feature)
                                if test_me not in vars_info_dict or instance not in vars_info_dict[test_me]:
                                        print("*****************var is none: ",lab_code_info.file_html)
                                        count_var_null += 1
                                        continue
                                if test_me not in size_obj_dict or instance not in size_obj_dict[test_me]:
                                        count_size_of_null+=1
                                        continue
                                one_instance_var_dict = vars_info_dict[test_me][instance]
                                if "file_html" not in dict_pd:
                                        dict_pd["file_html"] = [lab_code_info.file_html]
                                else:
                                        dict_pd["file_html"].append(lab_code_info.file_html)
                                if "test_me_inf" not in dict_pd:
                                        dict_pd["test_me_inf"] = [str(test_me)+str(instance)]
                                else:
                                        dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                                if "code_str" not in dict_pd:
                                        dict_pd['code_str'] = [lab_code_info.get_code_str()]
                                else:
                                        dict_pd['code_str'].append(lab_code_info.get_code_str())
                                perf_change_list.append(instance_feature['perf_change'][0])
                                if 'perf_change' not in dict_pd:
                                        dict_pd['perf_change'] = [instance_feature['perf_change'][0]]
                                else:
                                        dict_pd['perf_change'].append(instance_feature['perf_change'][0])
                                if 'perf_change_left' not in dict_pd:
                                        dict_pd['perf_change_left'] = [instance_feature['perf_change'][1]]
                                else:
                                        dict_pd['perf_change_left'].append(instance_feature['perf_change'][1])
                                if 'perf_change_right' not in dict_pd:
                                        dict_pd['perf_change_right'] = [instance_feature['perf_change'][2]]
                                else:
                                        dict_pd['perf_change_right'].append(instance_feature['perf_change'][2])
                                # get_FanIn_ExCall_Var_ExpVar(dict_pd,one_instance_var_dict,for_node)
                                get_FanIn_ExCall_Var_ExpVar_ast(dict_pd,one_instance_var_dict,for_node)
                                one_code_num_list.append(
                                        [instance_feature['num_ele'], int(size_obj_dict[test_me][instance][0]),
                                         instance_feature['perf_change'][0]])

                                for fea in dict_features:
                                        ele = dict_features[fea]  # np.log(dict_features[fea])
                                        if fea not in dict_pd:
                                                dict_pd[fea] = [ele]
                                        else:
                                                dict_pd[fea].append(ele)
                                count_instance += 1
                count_code += 1
                # print("one_code_num_list: ",one_code_num_list,count_size_of_null)
        print(">>>>>>>>features: ",dict_pd.keys())
        dataMain = pd.DataFrame(data=dict_pd)
        print(">>>>>>drop same features: ", dataMain.keys())
        # print(dataMain.to_dict())
        dataMain.to_csv(csv_feature_file_name_useful, index=False)
        # print("perf_change_list: ",perf_change_list)
        a=[]
        loop_num=len(perf_change_list)//10
        print("loop_num: ",loop_num)
        for i in range(loop_num):

                a.append(perf_change_list[i*10:(i+1)*10])
                for ind_instance,e in enumerate(perf_change_list[i*10:(i+1)*10]):
                        print(e)
                        if e>1:
                                # print(i, ind_instance,e, dict_pd["expVar_list"][i*10+ind_instance],dict_pd["Var_list"][i*10+ind_instance])
                                pass


        print(a)
        print(f"median {np.median(perf_change_list)}, min {np.min(perf_change_list)}, "
              f"max {np.max(perf_change_list)}, average {np.mean(perf_change_list)}, std {np.std(perf_change_list)}: ",)
        # dataMain = drop_rows_same(dataMain)
        # dataMain.to_csv(csv_feature_file_name_no_same, index=False)
        #"expVar_unique_list",
        dataMain.drop(columns=[ "expVar_list","Var_list", "FanIn_list", "externalCall_list"], inplace=True)
        # util.save_pkl(feature_info_dir, feature_file_name, dataMain.to_dict())
        # dataMain.to_csv(csv_feature_file_name, index=False)
        # dataMain = drop_rows_same(dataMain)



        print("count: ",file_code,count_code,count_test_me,count_instance,count_var_null,count_size_of_null,count_time_null)

def drop_rows_same(df):
        same_feature_list = []
        for index, row in df.iterrows():
                if row['file_html'] + row['code_str'] + str(row['num_ele']) in same_feature_list:
                        df.drop(index, inplace=True)
                else:
                        same_feature_list.append(row['file_html'] + row['code_str'] + str(row['num_ele']))
        return df
def remove_features():
        dict_pd = util.load_pkl(feature_info_dir, feature_file_name)

        # dict_pd["perf_change"] = np.log(dict_pd["perf_change"])
        stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
        # warnings.filterwarnings(action='once')
        warnings.filterwarnings(action='default')
        # load Data
        dataMain = pd.DataFrame(data=dict_pd)
        # print(dataMain.to_dict())
        # dataMain.to_csv(csv_feature_file_name, index=False)


        same_feature_list = []
        for key in dataMain:
                if len(set(dataMain[key])) <= 1:
                        # print(key)
                        same_feature_list.append(key)
                        # dataMain.drop
        print("same_feature_list: ", same_feature_list)
        dataMain.drop(columns=same_feature_list,inplace=True)
        print("all columns: ",dataMain.columns)
#"num_param","num_Delimiters","num_Keywords","FanIn","expVar","externalCall","num_Keywords","num_Delimiters","expVar","externalCall",
        remove_feature_list =\
                ["num_func_call","size_obj", "num_Delimiters","TotalVar","num_var",
                              "perf_change_left","perf_change_right",
                              "file_html","test_me_inf","code_str"]#['num_Delimiters','num_var','num_param','num_ele']
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
        # print(">>>>>>>>>>>corr:\n ",corr)
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
        print("dict_corr_num: ", sorted(dict_corr_num.items(), key=lambda kv: (kv[1], kv[0])),len(dataMain))
        print("features: ",dataMain.keys())
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
def get_sig_cliff():
        from scipy.stats import ranksums, mannwhitneyu
        import cliffsDelta
        bench_time_info_dir_list=["performance/list_compre_benchmarks_iter_improv_final_add_perf_change/",
                                  "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test/"]
        perf_change_list=[]

        for bench_time_info_dir_pre in bench_time_info_dir_list:
                bench_time_info_dir=util.data_root + bench_time_info_dir_pre
                a=[]
                for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                        file_name_no_suffix = file_name[:-4]

                        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                        lab_code_info: CodeInfo
                        for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info

                        file_html = lab_code_info.file_html
                        if file_html != "https://github.com/HunterMcGushion/hyperparameter_hunter/tree/master/hyperparameter_hunter/space/space_core.py":  # "https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv.py":
                                continue
                        total_time_list_info_dict = lab_code_info.total_time_list_info_dict
                        if not total_time_list_info_dict:
                                print(">>>>time is none ", file_name, lab_code_info.file_html)
                                continue
                        new_node_list = [new_tree]
                        if not remove_ass_flag:
                                new_node_list.append(assign_node)
                        for test_me in total_time_list_info_dict:
                                for instance in total_time_list_info_dict[test_me]:
                                        # total_time_list_info_dict = lab_code_info.get_stable_time_list(
                                        #         stable_info_dict=stable_info_dict)
                                        # # print("total_time_list_info_dict: ",total_time_list_info_dict)
                                        instance_feature = total_time_list_info_dict[test_me][instance]
                                        a.append(instance_feature['perf_change'][0])
                perf_change_list.append(a)
        print(mannwhitneyu(perf_change_list[0], perf_change_list[1]))
        d, res = cliffsDelta.cliffsDelta(perf_change_list[0], perf_change_list[1])
        print(d, res)



if __name__ == '__main__':

        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks/final_stable/"
        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_mod/prefined_cpus_remain_code/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_perf_change/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_perf_change/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_iter_improv_final/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change/"

        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_2/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_20invo/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_20invo_2/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_30invo/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_30invo_2/"
        save_code_info_dir_add_performance_change_list = [
                ["performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test/",
                 "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_2/"],
                ["performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_20invo/",
                 "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_20invo_2/"],
                ["performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_30invo/",
                 "performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_30invo_2/"]]
        dict_pd = dict()
        dict_pd_method = {"method_param": [], "mean_perf_change": [], "std_perf_change": [],
                          "median_perf_change": [], "max_perf_change": [], "min_perf_change": [],
                          "mean_perf_change_ratio": [], "std_perf_change_ratio": [],
                          "median_perf_change_ratio": [], "max_perf_change_ratio": [], "min_perf_change_ratio": [],
                          "sig": [], "cliff": [],
                          "mean_conf_ratio": [], "std_conf_ratio": [], "median_conf_ratio": [], "max_conf_ratio": [],
                          "min_conf_ratio": []}

        for file_1, file_2 in save_code_info_dir_add_performance_change_list:
                print("****************file: ", file_1, file_2)
                save_code_info_dir_add_performance_change_1 = util.data_root + file_1
                save_code_info_dir_add_performance_change_2 = util.data_root + file_2
        # for file_invo_dir in sorted(os.listdir(save_code_info_dir_add_performance_change_2)):
                # file_invo_dir="10"
                file_invo_dir=""
                invo_dir_path = save_code_info_dir_add_performance_change_1
                invo_dir_path_2 = save_code_info_dir_add_performance_change_2
                file_name_list = set(os.listdir(invo_dir_path)) & set(os.listdir(invo_dir_path_2))
                # save_features_1(invo_dir_path,file_name_list)
                # break
                file_html_list, num_ele_list, perf_change_list, perf_left_change_list, perf_right_change_list, conf_inter_list = save_perf_change(
                        invo_dir_path, file_name_list)
                _, _, perf_change_list_2, perf_left_change_list_2, perf_right_change_list_2, conf_inter_list_2 = save_perf_change(
                        invo_dir_path_2, file_name_list)
                conf_inter_ratio, conf_inter_ratio_2 = [e / perf_change_list[i] for i, e in
                                                        enumerate(conf_inter_list)], [e / perf_change_list_2[i]
                                                                                      for i, e in enumerate(
                                conf_inter_list_2)]
                dict_pd[file_1 + file_invo_dir + "file_html"] = file_html_list
                dict_pd[file_1 + file_invo_dir + "num_ele"] = num_ele_list
                dict_pd[file_1 + file_invo_dir + "_perf_change"] = perf_change_list
                dict_pd[file_1 + file_invo_dir + "_perf_left_change"] = perf_left_change_list
                dict_pd[file_1 + file_invo_dir + "_perf_right_change"] = perf_right_change_list
                dict_pd[file_1 + file_invo_dir + "_perf_confi_width_ratio"] = conf_inter_ratio
                dict_pd[file_2 + file_invo_dir + "_perf_change_2"] = perf_change_list_2
                dict_pd[file_2 + file_invo_dir + "_perf_left_change_2"] = perf_left_change_list_2
                dict_pd[file_2 + file_invo_dir + "_perf_right_change_2"] = perf_right_change_list_2
                dict_pd[file_2 + file_invo_dir + "_perf_confi_width_2_ratio"] = conf_inter_ratio_2
                dict_pd[file_2 + file_invo_dir + "_perf_change_diff"] = [abs(e - perf_change_list_2[ind_perf])
                                                                         for ind_perf, e in
                                                                         enumerate(perf_change_list)]
                dict_pd[file_2 + file_invo_dir + "_perf_confi_width_ratio_diff"] = [
                        abs(e - perf_change_list_2[ind_perf]) for ind_perf, e in enumerate(perf_change_list)]

                diff_mean_perf_change = [abs(e - perf_change_list_2[ind_perf]) for ind_perf, e in
                                         enumerate(perf_change_list)]
                diff_mean_perf_change_ratio = [abs(e - perf_change_list_2[ind_perf]) / e for ind_perf, e in
                                               enumerate(perf_change_list)]

                s, p_value = mannwhitneyu(perf_change_list, perf_change_list_2)
                d, res = cliffsDelta.cliffsDelta(perf_change_list, perf_change_list_2)
                dict_pd_method["method_param"].append(file_1 + str(file_invo_dir))

                dict_pd_method["mean_perf_change"].append(np.mean(diff_mean_perf_change))
                dict_pd_method["std_perf_change"].append(np.std(diff_mean_perf_change))
                dict_pd_method["median_perf_change"].append(np.median(diff_mean_perf_change))
                dict_pd_method["max_perf_change"].append(np.max(diff_mean_perf_change))
                dict_pd_method["min_perf_change"].append(np.min(diff_mean_perf_change))
                dict_pd_method["mean_perf_change_ratio"].append(np.mean(diff_mean_perf_change_ratio))
                dict_pd_method["std_perf_change_ratio"].append(np.std(diff_mean_perf_change_ratio))
                dict_pd_method["median_perf_change_ratio"].append(np.median(diff_mean_perf_change_ratio))
                dict_pd_method["max_perf_change_ratio"].append(np.max(diff_mean_perf_change_ratio))
                dict_pd_method["min_perf_change_ratio"].append(np.min(diff_mean_perf_change_ratio))
                dict_pd_method["sig"].append(p_value)
                dict_pd_method["cliff"].append(res)
                dict_pd_method["mean_conf_ratio"].append(np.mean(conf_inter_ratio))
                dict_pd_method["std_conf_ratio"].append(np.std(conf_inter_ratio))
                dict_pd_method["median_conf_ratio"].append(np.median(conf_inter_ratio))
                dict_pd_method["max_conf_ratio"].append(max(conf_inter_ratio))
                dict_pd_method["min_conf_ratio"].append(min(conf_inter_ratio))
                print("mean, std of diff perf change between two times: ", np.mean(diff_mean_perf_change),
                      np.std(diff_mean_perf_change), np.max(diff_mean_perf_change), np.mean(diff_mean_perf_change),
                      np.median(diff_mean_perf_change), np.min(diff_mean_perf_change))
                print("confidence width ratio: ", max(conf_inter_ratio), np.mean(conf_inter_ratio),
                      np.median(conf_inter_ratio), min(conf_inter_ratio))
                print("confidence width_2  ratio: ", max(conf_inter_ratio_2), np.mean(conf_inter_ratio_2),
                      np.median(conf_inter_ratio_2), min(conf_inter_ratio_2))
                print("sig: ", mannwhitneyu(perf_change_list, perf_change_list_2))

                print("cliffsDelta: ", d, res)
        dataMain = pd.DataFrame(data=dict_pd)
        # print(dataMain.to_dict())
        dataMain.to_csv("space_core_perf_change_list_comprehension.csv", index=False)

        dataMain = pd.DataFrame(data=dict_pd_method)
        # print(dataMain.to_dict())
        dataMain.to_csv("space_core_method_compare_list_comprehension.csv", index=False)

'''
        # feature_info_dir=util.data_root + "lab_performance/feature/list_compre_benchmarks/"
        feature_info_dir="./"
        feature_file_name="list_comprehension"
        feature_file_name="list_comprehension_original"
        feature_file_name="list_comprehension_original_complete_features"
        feature_file_name="list_compre_benchmarks_complete_features"
        feature_file_name="list_compre_benchmarks_complete_features_add_sizeof"
        feature_file_name="list_compre_benchmarks_complete_features_add_sizeof_correct_perf_change"
        feature_file_name="list_compre_benchmarks_complete_features_add_sizeof_correct_perf_change_callNoAppend"
        feature_file_name="list_compre_benchmarks_complete_features_add_sizeof_correct_perf_change_callNoAppend_add_FanIn_Call_ExpVa"
        feature_file_name="list_compre_benchmarks_complete_features_iterations_improve"

        csv_feature_file_name="labperformance_listcomprehension_complete_feature.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change_callNoAppend.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change_callNoAppend_no_same_feature_vector.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change_callNoAppend_no_same_feature_vector_add_FanIn_Call_ExpVa.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change_callNoAppend_no_same_feature_vector_add_FanIn_Call_ExpVa.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change_callNoAppend_no_same_feature_vector_add_FanIn_Call_ExpVa_all.csv"
        csv_feature_file_name="performance_list_compre_benchmarks_complete_features_iterations_improve.csv"

        csv_feature_file_name_useful="performance_listcomprehension_complete_feature_visualize.csv"
        csv_feature_file_name_useful="performance_list_compre_benchmarks_complete_features_iterations_improve_visualize.csv"
        csv_feature_file_name_useful="performance_list_compre_benchmarks_complete_features_iterations_improve_visualize_test.csv"


        csv_feature_file_name_no_same="performance_listcomprehension_complete_feature_visualize_no_same_feature.csv"
        csv_feature_file_name_no_same="performance_list_compre_benchmarks_complete_features_iterations_improve_visualize_no_same_feature.csv"

        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_corr.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector_add_FanIn_Call_ExpVa.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector_add_FanIn_Call_ExpVa_all.csv"
        csv_feature_file_name_corr="list_compre_benchmarks_complete_features_iterations_improve_corr.csv"

        
        sizeof_code_info_dir = util.data_root + "performance/list_compre_benchmarks_sizeof_feature/"
        dynamic_code_info_dir = util.data_root + "performance/list_compre_benchmarks_sizeof_type_num_ele_feature/"
        dynamic_code_info_dir = util.data_root + "performance/list_compre_benchmarks_sizeof_type_num_ele_feature_new/"
        save_features()
        # get_sig_cliff()
        # remove_features()
        # all_data_save()
        data=pd.read_csv(csv_feature_file_name).to_dict()
        print(list(data.keys()))
        '''

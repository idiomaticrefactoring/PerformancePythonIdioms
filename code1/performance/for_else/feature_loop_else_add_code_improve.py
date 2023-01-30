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
import util
import performance_util
import pandas as pd
from code_info import CodeInfo


def get_features(ast_node,if_node):
    node_kind=0 if isinstance(ast_node,ast.For) else 1
    has_else=1 if if_node.orelse else 0

    return node_kind,has_else
def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str_non_pythonic":[],
        "code_str_pythonic":[],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],

        "node_kind": [], 'has_else': []

    }# "branch_through_break": [], , "num_ele": [], "code_str": [], 'size_data':[],
    total_break=0
    total_code_instance=0
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):

        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
            # lab_code_info_add_num_ele = util.load_pkl(save_code_info_dir_num_ele, file_name_no_suffix)
            # lab_code_info_add_break = util.load_pkl(save_code_info_dir_add_isBreak, file_name_no_suffix)

        except:
            print(">>>> the file cannot load: ", save_code_info_dir_add_performance_change, file_name_no_suffix)
            continue
        try:
            lab_code_info_remove_outlier = util.load_pkl(save_code_info_dir_add_performance_change_remove_outlier,
                                                         file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ", save_code_info_dir_add_performance_change_remove_outlier,
                  file_name_no_suffix)
            continue
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py":
            # print(perf_info[0], "not valid file")
            continue
        print("file_name: ", file_name,file_html)
        code_str = lab_code_info.get_code_str()
        old_tree, new_tree, break_list_in_for, child, child_copy, \
        ass_init, if_varnode, init_ass_remove_flag = lab_code_info.code_info
        code_str_non_pythonic=ast.unparse(child)
        code_str_pythonic = ast.unparse(child_copy)
        # print("code: ",code_str_non_pythonic,code_str_pythonic)
        # break
        # print(lab_code_info.__dict__)
        perf_info_dict = lab_code_info.perf_info_dict
        # old_tree, new_tree, break_list_in_for, child, child_copy, \
        # ass_init, if_varnode, init_ass_remove_flag = lab_code_info.code_info
        # print("code: ",ast.unparse(old_tree),ast.unparse(if_varnode))
        node_kind,has_else=get_features(old_tree, if_varnode)
        # print("node_kind: ", node_kind,has_else)
        # continue
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        count_each_code=0
        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me)

                perf_info = perf_info_dict[test_me][instance]

                if perf_info[0]<0.9:
                    print(perf_info[0], "less than 0.9")
                    continue

                try:
                    perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]

                except:
                    continue
                # if file_html!="https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/measurements/fermion_partitioning.py":#"https://github.com/automl/SMAC3/tree/master/smac/facade/smac_ac_facade.py":
                #     continue
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
                # print(lab_code_info_add_num_ele.num_ele_list)
                # print(lab_code_info_add_break.num_ele_list)

                dict_pd["node_kind"].append(node_kind)
                dict_pd["has_else"].append(has_else)
                print("perf_info: ", file_name, test_me, perf_info)
                # print("perf_info: ", file_name, test_me, perf_info, perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))
                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                # dict_pd["code_str"].append(code_str)
                dict_pd["code_str_non_pythonic"].append(code_str_non_pythonic)
                dict_pd["code_str_pythonic"].append(code_str_pythonic)
                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])
                dict_pd["perf_change_rm_outlier"].append(perf_info_remove_outlier[0])
                dict_pd["perf_change_left_rm_outlier"].append(perf_info_remove_outlier[1])
                dict_pd["perf_change_right_rm_outlier"].append(perf_info_remove_outlier[2])
                dict_pd["RCIW"].append((perf_info[2] - perf_info[1]) / perf_info[0])
                dict_pd["RCIW_rm_outlier"].append(
                    (perf_info_remove_outlier[2] - perf_info_remove_outlier[1]) / perf_info_remove_outlier[0])
                count_each_code+=1

        print("number of code: ",file_name,count_each_code)
    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
    perf_change_zonghe_left_list = []
    perf_change_zonghe_right_list = []
    for i, e in enumerate(dict_pd['RCIW_rm_outlier']):
        if dict_pd['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_pd['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
            perf_change_zonghe_left_list.append(dict_pd["perf_change_left_rm_outlier"][i])
            perf_change_zonghe_right_list.append(dict_pd["perf_change_right_rm_outlier"][i])

        else:
            perf_change_zonghe_list.append(dict_pd['perf_change'][i])
            RCIW_zonghe_list.append(dict_pd['RCIW'][i])
            perf_change_zonghe_left_list.append(dict_pd["perf_change_left"][i])
            perf_change_zonghe_right_list.append(dict_pd["perf_change_right"][i])

    dict_pd["perf_change_zonghe"] = perf_change_zonghe_list
    dict_pd["RCIW_zonghe"] = RCIW_zonghe_list
    dict_pd["perf_change_right_zonghe"] = perf_change_zonghe_right_list
    dict_pd["perf_change_left_zonghe"] = perf_change_zonghe_left_list
    dict_pd["perf_change"] = perf_change_zonghe_list
    dict_pd["RCIW"] = RCIW_zonghe_list

    dataMain = pd.DataFrame(data=dict_pd, columns=['perf_change', "node_kind", 'has_else', 'size_data'])
    corr = dataMain.corr().to_dict()
    print(corr)
    # dataMain = pd.DataFrame(data=dict_pd)
    for key in dict_pd:
        feature = dict_pd[key]
        # average=feature.mean()
        # std = feature.std()
        try:
            a = scipy.stats.skew(feature)
            print("skew: ", key, a)
        except:
            print(f"the key {key} cannot compute the skew")
            traceback.print_exc()
        try:
            print(f"{key} max, min, median: ",np.max(dict_pd[key]),np.min(dict_pd[key]),np.mean(dict_pd[key]))
        except:
            print(f"the key {key} cannot compute the distribution of feature value")
    # print("total_break, total_code_instance: ",total_break, total_code_instance,total_break/total_code_instance)
    return dict_pd
def get_features_add_interval_remove_redudant(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],
        'size_data': [],
        "node_kind": [], 'has_else': []

    }# "branch_through_break": [], , "num_ele": [],
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        print("file_name: ", file_name)
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
            lab_code_info_add_num_ele = util.load_pkl(save_code_info_dir_num_ele, file_name_no_suffix)

        except:
            print(">>>> the file cannot load: ", save_code_info_dir_add_performance_change, file_name_no_suffix)
            continue
        try:
            lab_code_info_remove_outlier = util.load_pkl(save_code_info_dir_add_performance_change_remove_outlier,
                                                         file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ", save_code_info_dir_add_performance_change_remove_outlier,
                  file_name_no_suffix)
            continue
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        perf_info_dict = lab_code_info.perf_info_dict
        old_tree, new_tree, break_list_in_for, child, child_copy, \
        ass_init, if_varnode, init_ass_remove_flag = lab_code_info.code_info
        # print("code: ",ast.unparse(old_tree),ast.unparse(if_varnode))
        node_kind,has_else=get_features(old_tree, if_varnode)
        # print("node_kind: ", node_kind,has_else)
        # continue
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        count_each_code=0
        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                if file_html=="https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py":
                    continue
                # if file_html=="https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and instance==1:
                #     continue

                # print(test_me)
                if count_each_code>5:
                    break
                perf_info = perf_info_dict[test_me][instance]


                # if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and perf_info[0]<0.5:
                #     continue
                try:
                    perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
                except:
                    continue
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
                if test_me in lab_code_info_add_num_ele.num_ele_list:
                    num=lab_code_info_add_num_ele.num_ele_list[test_me][instance]
                    print("num: ",num)
                    dict_pd['size_data'].append(int(num[0]))
                else:
                    print(">>>>>>Wrong does not have ele: ",file_name)
                    continue
                dict_pd["node_kind"].append(node_kind)
                dict_pd["has_else"].append(has_else)
                print("perf_info: ", file_name, test_me, perf_info)
                # print("perf_info: ", file_name, test_me, perf_info, perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))
                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])
                dict_pd["perf_change_rm_outlier"].append(perf_info_remove_outlier[0])
                dict_pd["perf_change_left_rm_outlier"].append(perf_info_remove_outlier[1])
                dict_pd["perf_change_right_rm_outlier"].append(perf_info_remove_outlier[2])
                dict_pd["RCIW"].append((perf_info[2] - perf_info[1]) / perf_info[0])
                dict_pd["RCIW_rm_outlier"].append(
                    (perf_info_remove_outlier[2] - perf_info_remove_outlier[1]) / perf_info_remove_outlier[0])
                count_each_code+=1

        print("number of code: ",file_name,count_each_code)
    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
    perf_change_zonghe_left_list = []
    perf_change_zonghe_right_list = []
    for i, e in enumerate(dict_pd['RCIW_rm_outlier']):
        if dict_pd['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_pd['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
            perf_change_zonghe_left_list.append(dict_pd["perf_change_left_rm_outlier"][i])
            perf_change_zonghe_right_list.append(dict_pd["perf_change_right_rm_outlier"][i])

        else:
            perf_change_zonghe_list.append(dict_pd['perf_change'][i])
            RCIW_zonghe_list.append(dict_pd['RCIW'][i])
            perf_change_zonghe_left_list.append(dict_pd["perf_change_left"][i])
            perf_change_zonghe_right_list.append(dict_pd["perf_change_right"][i])

    dict_pd["perf_change_zonghe"] = perf_change_zonghe_list
    dict_pd["RCIW_zonghe"] = RCIW_zonghe_list
    dict_pd["perf_change_right_zonghe"] = perf_change_zonghe_right_list
    dict_pd["perf_change_left_zonghe"] = perf_change_zonghe_left_list
    dict_pd["perf_change"] = perf_change_zonghe_list
    dict_pd["RCIW"] = RCIW_zonghe_list

    dataMain = pd.DataFrame(data=dict_pd, columns=['perf_change', "node_kind", 'has_else'])
    corr = dataMain.corr().to_dict()
    print(corr)
    # dataMain = pd.DataFrame(data=dict_pd)
    for key in dict_pd:
        feature = dict_pd[key]
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
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change_new_remove_outlier/50/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_for_else/a_for_else_iter_invoca_add_perf_change_new_merge_remove_outlier_2/"

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/chain_compare_benchmarks_new/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_2/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change_new/50/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_else/a_for_else_iter_invoca_add_perf_change_new_merge_2/"
    save_code_info_dir_num_ele = util.data_root_mv + "performance/a_for_multi_tar_single_add_size_new/a_for_multi_tar_iter_invoca_2/"
    save_code_info_dir_num_ele = util.data_root_mv + "performance/a_for_else_add_size/a_for_else_tar_iter_invoca_2_once_again/"
    save_code_info_dir_add_isBreak = util.data_root_mv + "performance/a_for_else_add_isBreak/a_for_else_tar_iter_invoca_2_once_again/"

    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    # dict_pd=get_features_add_interval_remove_redudant(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)

    # csv_feature_file_name_corr= util.data_root_mv + "lab_performance/chain_compare_benchmarks_new/csv/train_data_chain_compare_new.csv"

    csv_perf_change_dir = util.data_root_mv + "performance/a_for_else/csv/"
    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_a_for_else.csv"
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_a_for_else_remove_redundant.csv"
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_a_for_else_add_size.csv"
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_a_for_else_add_size_code_improve.csv"

    # csv_feature_file_name_corr= csv_perf_change_dir+"train_data_a_for_else_remove_redundant_add_size.csv"

    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)
    print("number of dataset: ",len(dataMain["file_html"]))

    df_sample = dataMain.sample(n=133, random_state=2022)
    # df_sample.to_csv(dir_csv_feature + "sample_set_compre.csv", index=False)
    # df_sample.to_csv(dir_csv_feature + "sample_dict_compre.csv", index=False)
    # df_sample.to_csv(csv_perf_change_dir + "sample_loop_else.csv", index=False)
    # df_sample.to_csv(csv_perf_change_dir + "sample_loop_else_add_isBreak.csv", index=False)

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





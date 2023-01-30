import time
import traceback

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy
import matplotlib.pyplot as plt
import subprocess
import pandas as pd

import scipy.stats

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import matplotlib.pyplot as plt
import numpy as np
import util
import performance_util
import pandas as pd
from code_info import CodeInfo
def get_features(ast_node):
        dict_feature = {"num_loop": 0, "num_if": 0, "num_if_else": 0}
        num_call_with_name = 0
    # for ast_node in node_list:

        for node in ast.walk(ast_node):

            if isinstance(node, (ast.For, ast.While)):
                dict_feature["num_loop"] += 1
            elif isinstance(node, ast.If):
                if node.orelse:
                    dict_feature["num_if_else"] += 1
                else:
                    dict_feature["num_if"] += 1

        return dict_feature
def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [], "num_ele": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],
        'num_if': [], 'num_if_else': [],'num_loop': [],
        'context':[]

    }
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
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

        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.total_time_list_info_dict

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        perf_info_dict = lab_code_info.total_time_list_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        for_node, assign_node, remove_ass_flag, new_tree=lab_code_info.code_info

        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
                num_ele = perf_info_dict[test_me][instance]["num_ele"]
                perf_info = perf_info_dict[test_me][instance]["perf_change"]
                perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]["perf_change"]
                print("perf_info: ", file_name, test_me, perf_info, perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))
                dict_pd["num_ele"].append(int(num_ele))
                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)
                dict_feature_one = get_features(for_node)
                dict_pd["context"].append(1)
                for key_one in dict_feature_one:
                    dict_pd[key_one].append(dict_feature_one[key_one])

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])
                dict_pd["perf_change_rm_outlier"].append(perf_info_remove_outlier[0])
                dict_pd["perf_change_left_rm_outlier"].append(perf_info_remove_outlier[1])
                dict_pd["perf_change_right_rm_outlier"].append(perf_info_remove_outlier[2])
                dict_pd["RCIW"].append((perf_info[2] - perf_info[1]) / perf_info[0])
                dict_pd["RCIW_rm_outlier"].append(
                    (perf_info_remove_outlier[2] - perf_info_remove_outlier[1]) / perf_info_remove_outlier[0])
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
    dict_pd["RCIW"]=RCIW_zonghe_list

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

    # dataMain.to_csv(csv_feature_file_name_corr, index=False)
    # print("len of file and test methods: ",len(file_name_list),len(test_me_list))


    return dict_pd
def get_reason(dataMain):
    file_html=dataMain["file_html"]
    perf_change=dataMain["perf_change"]
    num_ele_list = dataMain["num_ele"]
    dataMain=dataMain.to_dict()
    dataMain['add_byte']=[0 for i in range(dataMain["perf_change"])]
    dataMain['remove_byte'] = [0 for i in range(dataMain["perf_change"])]
    dataMain['replace_unique_byte'] = [0 for i in range(dataMain["perf_change"])]
    dataMain['replace_byte'] = [0 for i in range(dataMain["perf_change"])]
    dataMain['replace_total_byte'] = [0 for i in range(dataMain["perf_change"])]
    unique_num=0
    add_num=0
    remove_num=0
    for ind,file_name in enumerate(file_html):
        if num_ele_list[ind]>=6:
            if perf_change[ind]>1:
                dataMain['remove_byte'][ind]=1
                remove_num+=1
            else:
                dataMain['add_byte'][ind] = 1
                add_num+=1
        else:
            if perf_change[ind]>1:
                dataMain['remove_byte'][ind]=1
                remove_num+=1
            else:
                dataMain['add_byte'][ind] = 1
                add_num+=1
    sum_num=unique_num+remove_num+add_num

    print(unique_num,remove_num,add_num)
    print(unique_num/sum_num, remove_num/sum_num, add_num/sum_num)
if __name__ == '__main__':
    # bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    # total_file_list = [e[:-3] for e in os.listdir(bench_dir)]
    bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    total_filter_file_name_list=[]
    for e in os.listdir(bench_dir):
        total_filter_file_name_list.append(e[:-3])
    print(total_filter_file_name_list[0],len(total_filter_file_name_list))
    #'''
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3_improve/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/dict_compre_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new_add_perf_change_remove_outlier/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/prefined_cpus_remain_code_new_add_perf_change_remove_outlier/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_2_50_invocations/"

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/dict_compre_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_2nd_invo_step_100/50/"

    dir_csv_feature = util.data_root_mv + "performance/a_list_comprehension/csv/"
    csv_feature_file_name_corr = dir_csv_feature + "train_data_list_compre.csv"
    if not os.path.exists(dir_csv_feature):
        os.makedirs(dir_csv_feature)


    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)

    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)
    df_sample = dataMain.sample(n=253, random_state=2022)
    df_sample.to_csv(dir_csv_feature + "sample_list_comp_perf.csv", index=False)
    # get_reason(dataMain)




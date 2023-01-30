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


def get_features(ast_node):
    dict_feature =  {'num_cmpop': 0, "num_true": 0, "num_Lt": 0, "num_Gt": 0,
        "num_Eq": 0, "num_NotEq": 0, "num_LtE": 0, "num_GtE": 0, "num_NotIn": 0, "num_In":0, "num_Is": 0,
        "num_IsNot": 0}
    num_call_with_name = 0
    # for ast_node in node_list:
    cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


    for node in ast.walk(ast_node):
        if isinstance(node,ast.Compare):
            if len(node.ops)>1:
                for cmpop in node.ops:
                    if isinstance(cmpop,ast.Eq):
                        cmpop_1 += 1
                    elif  isinstance(cmpop,ast.NotEq):
                        cmpop_2 += 1
                    elif isinstance(cmpop,ast.LtE):
                        cmpop_3 += 1
                    elif isinstance(cmpop,ast.GtE):
                        cmpop_4 += 1
                    elif isinstance(cmpop,ast.Lt):
                        cmpop_5 += 1
                    elif isinstance(cmpop,ast.Gt):
                        cmpop_6 += 1
                    elif isinstance(cmpop,ast.NotIn):
                        cmpop_7 += 1
                    elif isinstance(cmpop,ast.In):
                        cmpop_8 += 1
                    elif isinstance(cmpop,ast.Is):
                        cmpop_9 += 1
                    elif isinstance(cmpop,ast.IsNot):
                        cmpop_10 += 1
                break


    return cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10
def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],

         "num_Lt": [], "num_Gt": [],
        "num_Eq": [], "num_NotEq": [], "num_LtE": [], "num_GtE": [], "num_NotIn": [], "num_In": [], "num_Is": [],
        "num_IsNot": []

    }
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        print("file_name: ", file_name)
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
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        # if file_html=="https://github.com/capitalone/DataProfiler/tree/master/dataprofiler/profilers/helpers/report_helpers.py" or \
        #     file_html=="https://github.com/makepath/xarray-spatial/tree/master/xrspatial/pathfinding.py" or \
        # file_html=="https://github.com/bayespy/bayespy/tree/master/bayespy/utils/optimize.py":
        #     continue
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        perf_info_dict = lab_code_info.perf_info_dict
        old_tree, new_tree = lab_code_info.code_info
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10 = get_features(
            new_tree)
        print(ast.unparse(new_tree),cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10 )
        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me)

                perf_info = perf_info_dict[test_me][instance]


                # if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and perf_info[0]<0.5:
                #     continue
                try:
                    perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
                except:
                    continue
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
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

    dataMain = pd.DataFrame(data=dict_pd, columns=['perf_change',  "num_Lt", "num_Gt",
        "num_Eq", "num_NotEq", "num_LtE", "num_GtE", "num_NotIn", "num_In", "num_Is",
        "num_IsNot"])
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
def get_features_add_interval_remove_redudant(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],

        "num_Lt": [], "num_Gt": [],
        "num_Eq": [], "num_NotEq": [], "num_LtE": [], "num_GtE": [], "num_NotIn": [], "num_In": [], "num_Is": [],
        "num_IsNot": []

    }
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        print("file_name: ", file_name)
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
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        # if file_html=="https://github.com/capitalone/DataProfiler/tree/master/dataprofiler/profilers/helpers/report_helpers.py" or \
        #     file_html=="https://github.com/makepath/xarray-spatial/tree/master/xrspatial/pathfinding.py" or \
        # file_html=="https://github.com/bayespy/bayespy/tree/master/bayespy/utils/optimize.py":
        #     continue
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        perf_info_dict = lab_code_info.perf_info_dict
        old_tree, new_tree = lab_code_info.code_info
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        count_each_code=0

        cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10 = get_features(
            new_tree)
        print(ast.unparse(new_tree), cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9,
              cmpop_10)
        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me)

                perf_info = perf_info_dict[test_me][instance]
                if count_each_code>5:
                    break
                # if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and perf_info[0]<0.5:
                #     continue
                try:
                    perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
                except:
                    continue
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
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
                count_each_code += 1
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

    dataMain = pd.DataFrame(data=dict_pd, columns=['perf_change', "num_Lt", "num_Gt",
                                                   "num_Eq", "num_NotEq", "num_LtE", "num_GtE", "num_NotIn", "num_In",
                                                   "num_Is",
                                                   "num_IsNot"])
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

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/chain_compare_benchmarks_new/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_2/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change_new/50/"

    # dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    # csv_feature_file_name_corr= util.data_root_mv + "lab_performance/chain_compare_benchmarks_new/csv/train_data_chain_compare_new.csv"
    dict_pd=get_features_add_interval_remove_redudant(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)


    csv_perf_change_dir = util.data_root_mv + "performance/chain_compare/csv/"
    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_chain_compare_new_3.csv"
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_chain_compare_new_3_remove_redundant.csv"

    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)
    print("number of dataset: ",len(dataMain["file_html"]))
    #
    # df_sample = dataMain.sample(n=329, random_state=2022)
    # # df_sample.to_csv(dir_csv_feature + "sample_set_compre.csv", index=False)
    # # df_sample.to_csv(dir_csv_feature + "sample_dict_compre.csv", index=False)
    # df_sample.to_csv(csv_perf_change_dir + "sample_chain_compare.csv", index=False)
    from sklearn.utils import shuffle

    dataMain = shuffle(dataMain,random_state=2022)
    dataMain.reset_index(inplace=True, drop=True)
    df_sample = dataMain.sample(n=329, random_state=2022)
    # df_sample.to_csv(dir_csv_feature + "sample_set_compre.csv", index=False)
    # df_sample.to_csv(dir_csv_feature + "sample_dict_compre.csv", index=False)
    # df_sample.to_csv(csv_perf_change_dir + "sample_chain_compare_new.csv", index=False)
    df_sample.to_csv(csv_perf_change_dir + "sample_chain_compare_new_remove_reduandant.csv", index=False)

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





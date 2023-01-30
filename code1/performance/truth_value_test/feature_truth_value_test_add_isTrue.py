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


def get_features(file_html,repo_name,old_tree):
    empty = ast.unparse(old_tree)
    comp_op=-1
    for node_comp in ast.walk(old_tree):
        if isinstance(node_comp, ast.Compare):
            ops=node_comp.ops
            for op in ops:
                if isinstance(op,ast.Eq):
                    comp_op=1
                    pass
                elif isinstance(op,ast.NotEq):
                    comp_op = 0
                    pass
                else:
                    pass
                    # print(">>>>>>>>>>please check the data",ast.unparse(old_tree))
            #
            left_str = ast.unparse(node_comp.left)
            if left_str in dict_empty_set.keys():
                empty = left_str
                break
            for compara in node_comp.comparators:
                compara_str = ast.unparse(compara)
                if compara_str in dict_empty_set.keys():
                    empty = compara_str
                    break
            break
    pro_path = util.data_root + "python_star_2000repo/"
    repo_path = pro_path + repo_name + "/"
    real_file_html = file_html.replace("//", "/")
    rela_path = real_file_html.split("/")[6:]
    old_path = repo_path + "/".join(rela_path)
    content = util.load_file_path(old_path)
    node_kind = -1
    for node in ast.walk(ast.parse(content)):
        try:
            if node.lineno == old_tree.lineno:
                # print("content: ",ast.unparse(node))
                if isinstance(node, ast.If):
                    node_kind = 0
                    # print("got if it: ", ast.unparse(node))
                    pass
                elif isinstance(node, ast.While):
                    node_kind = 1

                    # print("got while it: ", ast.unparse(node))
                    pass
                elif isinstance(node, ast.Assert):
                    node_kind = 2

                    # print("got assert it: ", ast.unparse(node))
                    pass

                break
        except:
            continue
    print(node_kind,empty,comp_op)
    return node_kind,empty,comp_op

def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],

        "comp_op": [], 'node_kind': [],
        "is_None": [], "is_False": [], "is_0": [], "is_0.0": [], "is_0j": [], "is_Decimal(0)": [],
        "is_Fraction(0, 1)": [], "is_empty_string": [], "is_()": [], "is_[]": [], "is_{}": [],
        "is_dict()": [], "is_set()": [], "is_range(0)": [],'isTrue_executepath':[]


    }
    file_html_list=[]
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        print("file_name: ", file_name)
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
            lab_code_info_add_isTrue = util.load_pkl(isTrue_code_info_dir, file_name_no_suffix)

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

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        # if file_html!="https://github.com/Nikolay-Kha/PyCNC/tree/master/cnc/hal_virtual.py":
        #     continue
        repo_name=lab_code_info.repo_name
        old_tree, new_tree = lab_code_info.code_info
        node_kind,empty,comp_op=get_features(file_html, repo_name, old_tree)
        code_str = lab_code_info.get_code_str()
        # print(ast.unparse(old_tree),ast.unparse(new_tree))

        # continue
        perf_info_dict = lab_code_info.perf_info_dict
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        # print(empty)
        # if 1:
        # cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10 = get_features(
        #     new_tree)
        # print(ast.unparse(new_tree),cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10 )
        #
        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me)
                try:
                    perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
                except:
                    continue
                if test_me in lab_code_info_add_isTrue.num_ele_list:
                    if instance < len(lab_code_info_add_isTrue.num_ele_list[test_me]):# and instance < len(lab_code_info_add_break.num_ele_list[test_me]):
                        num=lab_code_info_add_isTrue.num_ele_list[test_me][instance]

                        dict_pd['isTrue_executepath'].append(int(num[0]))
                    else:
                        print(">>>>>>Wrong does not have ele: ",instance, file_html,file_name,len(lab_code_info_add_isTrue.num_ele_list[test_me][0]),len(lab_code_info_add_isTrue.num_ele_list[test_me]))
                        continue
                else:
                    print(">>>>>>test_me,Wrong does not have ele: ",file_html,file_name)
                    continue
                perf_info = perf_info_dict[test_me][instance]


                # if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and perf_info[0]<0.5:
                #     continue

                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)

                for key in dict_empty_set:
                    key_f = dict_empty_set[key]
                    if key == "empty_string":
                        if "''" == empty:
                            dict_pd[key_f].append(1)
                        else:
                            dict_pd[key_f].append(0)
                    else:
                        if key == empty:
                                dict_pd[key_f].append(1)
                        else:
                                dict_pd[key_f].append(0)
                dict_pd["node_kind"].append(node_kind)
                dict_pd["comp_op"].append(comp_op)
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
        file_html_list.append(file_html)
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

    dataMain = pd.DataFrame(data=dict_pd, columns=["comp_op", 'node_kind',
        "is_None", "is_False", "is_0", "is_0.0", "is_0j", "is_Decimal(0)",
        "is_Fraction(0, 1)", "is_empty_string", "is_()", "is_[]", "is_{}",
        "is_dict()", "is_set()", "is_range(0)"])
    corr = dataMain.corr().to_dict()
    # print(corr)
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

    util.save_json(file_html_dir,"all_file_html_truth_test",file_html_list)
    return dict_pd
if __name__ == '__main__':
    # bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    # total_file_list = [e[:-3] for e in os.listdir(bench_dir)]
    dict_empty_set = {"None": "is_None", "False": "is_False", "0": "is_0", "0.0": "is_0.0", "0j": "is_0j",
                      "Decimal(0)": "is_Decimal(0)", "Fraction(0, 1)": "is_Fraction(0, 1)",
                      "empty_string": "is_empty_string", "()": "is_()", "[]": "is_[]", "{}": "is_{}",
                      "dict()": "is_dict()", "set()": "is_set()", "range(0)": "is_range(0)"}

    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3_improve/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/chain_compare_benchmarks_new/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_2/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change_new_remove_outlier/50/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_remove_outlier_total_data/"

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/chain_compare_benchmarks_new/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_2/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change_new/50/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_total_data/"
    file_html_dir=util.data_root_mv + "performance/a_truth_value_test/"
    isTrue_code_info_dir = util.data_root_mv + "performance/a_truth_value_test_isTrue/a_truth_value_test_iter_invoca_total_data/"

    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    # csv_feature_file_name_corr= util.data_root_mv + "lab_performance/chain_compare_benchmarks_new/csv/train_data_chain_compare_new.csv"

    csv_perf_change_dir = util.data_root_mv + "performance/a_truth_value_test/csv/"
    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_truth_value_test.csv"

    dataMain = pd.DataFrame(data=dict_pd)
    # dataMain.to_csv(csv_feature_file_name_corr, index=False)
    print("number of dataset: ",len(dataMain["file_html"]))

    df_sample = dataMain.sample(n=381, random_state=2022)
    # df_sample.to_csv(dir_csv_feature + "sample_set_compre.csv", index=False)
    # df_sample.to_csv(dir_csv_feature + "sample_dict_compre.csv", index=False)
    # df_sample.to_csv(csv_perf_change_dir + "sample_truth_value_test.csv", index=False)

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





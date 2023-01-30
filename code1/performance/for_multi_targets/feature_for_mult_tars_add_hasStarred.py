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
from extract_transform_complicate_code_new.extract_compli_var_unpack_for_target_improve_new import get_for_target_add_info,get_for_target


def get_features(old_tree,new_tree):
    num_star, num_unpack, num_subscript, dim_subscript=0,0,0,0
    new_code_list = get_for_target_add_info(old_tree)
    # print(old_tree)
    target_str=ast.unparse(new_tree.target)
    num_star=target_str.count("*")
    for old_tree, new_tree, var_list_real, Map_Var in new_code_list:
        var_list_real_str = [ast.unparse(e) for e in var_list_real]
        # print("old_tree: ", ast.unparse(old_tree))
        # print("new_tree: ", ast.unparse(new_tree))
        # print("Map_Var: ", Map_Var)
        # print("var_list_real: ", var_list_real)
        for k_node in ast.walk(var_list_real[0]):
            if isinstance(k_node,ast.Subscript):
                dim_subscript+=1
        num_unpack=len(set(var_list_real_str))
        num_subscript=len(var_list_real_str)
        # dict_pd["num_unpack"].append(len(set(var_list_real_str)))
        # dict_pd["num_subscript"].append(len(var_list_real_str))




    print( num_star, num_unpack, num_subscript, dim_subscript)
    return num_star, num_unpack, num_subscript, dim_subscript

def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],
        'num_star': [], "num_unpack": [], "num_subscript": [], "dim_subscript": [],
          'size_data':[]

    }#"num_ele": [], context
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        # if file_name!="ngxtop.config_parser.get_log_formats_0.pkl":
        #     continue
        print("file_name: ", file_name)
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
            lab_code_info_add_num_ele = util.load_pkl(save_code_info_dir_num_ele, file_name_no_suffix)
            # print(lab_code_info_add_num_ele.num_ele_list)

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
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        old_tree, new_tree = lab_code_info.code_info
        # print("file_name: ", file_name, ast.unparse(old_tree),ast.unparse(new_tree))#[ast.unparse(e) for e in old_tree])

        num_star, num_unpack, num_subscript, dim_subscript=get_features(old_tree, new_tree)
        # continue
        # continue
        # for e in old_tree:
        #     value_node=e.value
        #     if not isinstance(value_node, ast.Constant):
        #         # print(">>>>>>yes: is not constant ")
        #         is_const=0
        #         break
        # 'is_step_1'        # continue
        perf_info_dict = lab_code_info.perf_info_dict
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        # if 1:

        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me,lab_code_info_add_num_ele.num_ele_list,instance,perf_info_dict[test_me])

                    # print(">>>>>>>ele: ",num)
                perf_info = perf_info_dict[test_me][instance]

                # continue
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
                dict_pd["dim_subscript"].append(dim_subscript)
                dict_pd["num_star"].append(num_star)
                dict_pd["num_unpack"].append(num_unpack)
                dict_pd["num_subscript"].append(num_subscript)


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

    dataMain = pd.DataFrame(data=dict_pd, columns=['num_subscript',
        "num_star", 'dim_subscript', 'num_unpack','size_data'])#'num_star': [], "num_unpack": [], "num_subscript": [], "dim_subscript"
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


    return dict_pd
def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],
        'num_star': [], "num_unpack": [], "num_subscript": [], "dim_subscript": [],
          'size_data':[],'hasStarred':[]

    }#"num_ele": [], context
    file_html_list = []

    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        # if file_name!="ngxtop.config_parser.get_log_formats_0.pkl":
        #     continue
        print("file_name: ", file_name)
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
            lab_code_info_add_num_ele = util.load_pkl(save_code_info_dir_num_ele, file_name_no_suffix)
            # print(lab_code_info_add_num_ele.num_ele_list)



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
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        old_tree, new_tree = lab_code_info.code_info
        # print("file_name: ", file_name, ast.unparse(old_tree),ast.unparse(new_tree))#[ast.unparse(e) for e in old_tree])

        num_star, num_unpack, num_subscript, dim_subscript=get_features(old_tree, new_tree)
        # continue
        # continue
        # for e in old_tree:
        #     value_node=e.value
        #     if not isinstance(value_node, ast.Constant):
        #         # print(">>>>>>yes: is not constant ")
        #         is_const=0
        #         break
        # 'is_step_1'        # continue
        perf_info_dict = lab_code_info.perf_info_dict
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        # if 1:

        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me,lab_code_info_add_num_ele.num_ele_list,instance,perf_info_dict[test_me])

                    # print(">>>>>>>ele: ",num)
                perf_info = perf_info_dict[test_me][instance]

                # continue
                # if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and perf_info[0]<0.5:
                #     continue
                try:
                    perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
                    # len_star=0
                    # for key in lab_code_info_add_num_ele.num_ele_list:
                    #     len_star = max(len_star,max([int(e) for e in lab_code_info_add_num_ele.num_ele_list[key][0]]))
                    #     print(file_html,lab_code_info_add_num_ele.num_ele_list)
                    #     # break
                    len_star = max([int(e) for e in lab_code_info_add_num_ele.num_ele_list[test_me][0]])

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
                dict_pd["dim_subscript"].append(dim_subscript)
                dict_pd["num_star"].append(num_star)
                dict_pd["num_unpack"].append(num_unpack)
                dict_pd["num_subscript"].append(num_subscript)
                old_tree, new_tree = lab_code_info.code_info

                target_str = ast.unparse(new_tree.target)
                count_target = target_str.count(", ") - target_str.count("*") + 1
                print("starred: ",ast.unparse(new_tree),len_star,count_target)

                if count_target == len_star:
                    dict_pd["hasStarred"].append(0)
                else:
                    dict_pd["hasStarred"].append(1)

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

    dataMain = pd.DataFrame(data=dict_pd, columns=['num_subscript',
        "num_star", 'dim_subscript', 'num_unpack','size_data'])#'num_star': [], "num_unpack": [], "num_subscript": [], "dim_subscript"
    corr = dataMain.corr().to_dict()
    print(corr)
    util.save_json(file_html_dir,"all_file_html_for_multi_tar",file_html_list)

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


    return dict_pd
def get_features_add_interval_remove_redundant(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],
        'num_star': [], "num_unpack": [], "num_subscript": [], "dim_subscript": [],
          'size_data':[]

    }#"num_ele": [], context
    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        # if file_name!="ngxtop.config_parser.get_log_formats_0.pkl":
        #     continue
        print("file_name: ", file_name)
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
            lab_code_info_add_num_ele = util.load_pkl(save_code_info_dir_num_ele, file_name_no_suffix)
            # print(lab_code_info_add_num_ele.num_ele_list)

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
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        old_tree, new_tree = lab_code_info.code_info
        # print("file_name: ", file_name, ast.unparse(old_tree),ast.unparse(new_tree))#[ast.unparse(e) for e in old_tree])

        num_star, num_unpack, num_subscript, dim_subscript=get_features(old_tree, new_tree)
        # continue
        # continue
        # for e in old_tree:
        #     value_node=e.value
        #     if not isinstance(value_node, ast.Constant):
        #         # print(">>>>>>yes: is not constant ")
        #         is_const=0
        #         break
        # 'is_step_1'        # continue
        perf_info_dict = lab_code_info.perf_info_dict
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        # if 1:
        count_each_code = 0
        all_test_instance_perf_list = []
        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me,lab_code_info_add_num_ele.num_ele_list,instance,perf_info_dict[test_me])

                    # print(">>>>>>>ele: ",num)
                perf_info = perf_info_dict[test_me][instance]

                # continue
                # if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and perf_info[0]<0.5:
                #     continue
                try:
                    perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
                except:
                    continue
                perf_one = perf_info[0]
                perf_one_rm = perf_info_remove_outlier[0]
                rciw_one = (perf_info[2] - perf_info[1]) / perf_info[0]
                rciw_one_rm = (perf_info_remove_outlier[2] - perf_info_remove_outlier[1]) / perf_info_remove_outlier[0]
                if rciw_one > rciw_one_rm:
                    if instance == 0:
                        all_test_instance_perf_list.append(perf_one_rm)
                        perf_change_zonghe_list.append(perf_one_rm)
                        RCIW_zonghe_list.append(rciw_one_rm)
                    else:

                        if abs(np.mean(all_test_instance_perf_list) - perf_one_rm) > 0.2:
                            all_test_instance_perf_list.append(perf_one_rm)
                            perf_change_zonghe_list.append(perf_one_rm)
                            RCIW_zonghe_list.append(rciw_one_rm)
                        else:
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
                dict_pd["dim_subscript"].append(dim_subscript)
                dict_pd["num_star"].append(num_star)
                dict_pd["num_unpack"].append(num_unpack)
                dict_pd["num_subscript"].append(num_subscript)


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

    dataMain = pd.DataFrame(data=dict_pd, columns=['num_subscript',
        "num_star", 'dim_subscript', 'num_unpack','size_data'])#'num_star': [], "num_unpack": [], "num_subscript": [], "dim_subscript"
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
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_multi_assign/a_multi_assign_iter_invoca_add_perf_change_new_remove_outlier_merge/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_call_star_single_2/a_call_star_single_iter_invoca_add_perf_change_new_merge_remove_outlier_2_new/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_for_multi_tar_single_2/a_for_multi_tar_iter_invoca_add_perf_change_new_merge_2_remove_outlier/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_multi_tar_single_3_new/a_for_multi_tar_iter_invoca_add_perf_change_new_merge_2_remove_outlier/"

    file_html_dir=util.data_root_mv + "performance/a_for_multi_tar_single_2/"

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/chain_compare_benchmarks_new/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_2/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change_new/50/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_multi_assign/a_multi_assign_iter_invoca_add_perf_change_new_merge/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_call_star_single_2/a_call_star_single_iter_invoca_add_perf_change_new_merge_2_new/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_multi_tar_single_2/a_for_multi_tar_iter_invoca_add_perf_change_new_merge_2/"
    # save_code_info_dir_num_ele=util.data_root_mv+"performance/a_for_multi_tar_single_add_size/a_for_multi_tar_iter_invoca_2/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_multi_tar_single_3_new/a_for_multi_tar_iter_invoca_add_perf_change_new_merge_2/"

    save_code_info_dir_num_ele=util.data_root_mv + "performance/a_for_multi_tar_single_add_size_new/a_for_multi_tar_iter_invoca_2/"

    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    # csv_feature_file_name_corr= util.data_root_mv + "lab_performance/chain_compare_benchmarks_new/csv/train_data_chain_compare_new.csv"

    csv_perf_change_dir = util.data_root_mv + "performance/a_for_multi_tar_single_2/csv/"
    csv_perf_change_dir = util.data_root_mv + "performance/a_for_multi_tar_single_3_new/csv/"

    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_for_multi_tar.csv"
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_for_multi_tar_add_size_data_add_hasStarred.csv"

    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)

    print("number of dataset: ", len(dataMain["file_html"]))

    df_sample = dataMain.sample(n=179, random_state=2022)
    # df_sample.to_csv(csv_perf_change_dir + "sample_for_multi_tar_perf.csv", index=False)

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





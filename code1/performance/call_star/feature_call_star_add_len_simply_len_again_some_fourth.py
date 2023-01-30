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


def get_features(old_tree,new_tree):
    print(">>>>>>: ", [ast.unparse(old_node) for old_node in old_tree], new_tree, new_tree.__dict__,
          ast.unparse(new_tree), new_tree.value.value)
    value_left=new_tree.value.value.value
    if isinstance(value_left,ast.Subscript):
        dim_subscript=2
    else:
        dim_subscript = 1
    if new_tree.value.value.slice.step:
        is_step_1=0
        print("step is not 1")
    else:
        is_step_1 = 1
    num_subscript, is_value_const, is_lower_0, is_upper_len=-1,0,0,0
    # for ast_node in node_list:

    # for e_sub in old_tree[]:
    slice=old_tree[0].slice
    num_subscript=len(old_tree)
    if isinstance(slice,ast.Constant):
            is_value_const=1
            if ast.unparse(slice)=='0':
                is_lower_0=1
                print("lower is 0: ",ast.unparse(old_tree))
    print(dim_subscript,num_subscript, is_value_const, is_lower_0, is_upper_len)
    return dim_subscript,num_subscript, is_value_const, is_lower_0, is_upper_len,is_step_1

def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf": [], "instance": [], "code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [],
        'RCIW_rm_outlier': [],
        'num_subscript': [],
        "is_value_const": [], 'is_lower_1': [], 'is_upper_len': [],
        'is_step_1':[],'has_Subscript':[],"has_Upper":[]

    }#"num_ele": [], context
    file_html_list = []

    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        print("file_name: ", file_name)
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)

            str_file_name = "_".join(file_name_no_suffix.split("_")[:-1]) + "_"
            new_file_name = str_file_name + str(int(file_name_no_suffix.split("_")[-1]) + 55)

            lab_code_info_add_num_ele = util.load_pkl(save_code_info_dir_len, new_file_name)

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
        arg_list, new_tree = lab_code_info_add_num_ele.code_info
        old_tree = arg_list[0]
        call_node = arg_list[-2]
        dim_subscript,num_subscript,is_value_const,is_lower_0,is_upper_len,is_step_1=get_features(old_tree,new_tree)

        print("file_name: ", file_name, [ast.unparse(e) for e in old_tree],ast.unparse(call_node),ast.unparse(new_tree),new_tree.value)#[ast.unparse(e) for e in old_tree])
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

        def get_is_upper_has_subscript(lab_code_info, len_node):

            arg_list, new_node = lab_code_info.code_info
            node_list = arg_list[0]
            # call_node = arg_list[-2]
            print(new_node, ast.unparse(new_node), new_node.__dict__, new_node.value.value.slice,
                  hasattr(new_node.value.value.slice, 'lower'))
            # lower =new_node.value.value.slice.lower

            lower_value = ast.unparse(new_node.value.value.slice.lower) if new_node.value.value.slice.lower else '0'
            # lower_value = ast.unparse(lower)
            # if lower_value == '0':
            #     new_node.value.value.slice.lower = None
            if lower_value.isdigit():
                if len_node - int(lower_value) == len(node_list):

                    upper = new_node.value.value.slice.upper
                    step = new_node.value.value.slice.step
                    new_node.value.value.slice.upper = None
                    if lower_value == '0' and not step or lower_value == '0' and ast.unparse(step) == '1':
                        # new_node = new_node.subscript.value.value.value
                        print("has_Upper,has_Subscript: ", 0, 0)
                        return 0, 0
                    else:
                        print("has_Upper,has_Subscript: ", 0, 1)
                        return 0, 1
            print("has_Upper,has_Subscript: ", 1, 1)
            return 1, 1
        # if 1:
        count_each_code=0
        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me)

                perf_info = perf_info_dict[test_me][instance]
                if perf_info[0]<0.5:
                    print("perf less than 0.5")
                    continue

                # if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and perf_info[0]<0.5:
                #     continue
                try:
                    perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
                except:
                    continue

                if test_me in lab_code_info_add_num_ele.num_ele_list:
                    if instance < len(lab_code_info_add_num_ele.num_ele_list[test_me]):# and instance < len(lab_code_info_add_break.num_ele_list[test_me]):
                        num=lab_code_info_add_num_ele.num_ele_list[test_me][instance]
                        has_Upper,has_Subscript=get_is_upper_has_subscript(lab_code_info_add_num_ele, int(num[0]))
                        dict_pd['has_Subscript'].append(has_Subscript)
                        dict_pd['has_Upper'].append(has_Upper)
                    else:
                        print(">>>>>>Wrong does not have ele: ",instance, file_html,file_name,len(lab_code_info_add_num_ele.num_ele_list[test_me][0]),len(lab_code_info_add_isTrue.num_ele_list[test_me]))
                        continue
                else:
                    print(">>>>>>test_me,Wrong does not have ele: ",file_html,file_name)
                    continue

                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
                dict_pd["num_subscript"].append(num_subscript)
                dict_pd["is_value_const"].append(is_value_const)
                dict_pd["is_lower_1"].append(is_lower_0)
                dict_pd["is_upper_len"].append(is_upper_len)
                dict_pd["is_step_1"].append(is_step_1)

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
        print("number of code: ", file_name, count_each_code)
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
        "is_value_const", 'is_lower_1', 'is_upper_len',
        'is_step_1'])
    corr = dataMain.corr().to_dict()
    print(corr)
    # dataMain = pd.DataFrame(data=dict_pd)
    util.save_json(file_html_dir,"all_file_html_call_star",file_html_list)

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
        'num_subscript': [],"dim_subscript":[],
        "is_value_const": [], 'is_lower_1': [], 'is_upper_len': [],
        'is_step_1':[]

    }#"num_ele": [], context
    file_name_list = set([])
    test_me_list = set([])
    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
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

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        arg_list, new_tree = lab_code_info.code_info
        old_tree = arg_list[0]
        call_node = arg_list[-2]
        dim_subscript,num_subscript,is_value_const,is_lower_0,is_upper_len,is_step_1=get_features(old_tree,new_tree)

        print("file_name: ", file_name, [ast.unparse(e) for e in old_tree],ast.unparse(call_node),ast.unparse(new_tree),new_tree.value)#[ast.unparse(e) for e in old_tree])
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
        count_each_code=0
        all_test_instance_perf_list=[]

        for ind_tm, test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me)
                if len(all_test_instance_perf_list)>10:
                    break
                perf_info = perf_info_dict[test_me][instance]


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

                    # all_test_instance_perf_list.append(perf_one_rm)



                else:
                    if instance == 0:
                        all_test_instance_perf_list.append(perf_one)
                        perf_change_zonghe_list.append(perf_one)
                        RCIW_zonghe_list.append(rciw_one)
                    else:
                        if abs(np.mean(all_test_instance_perf_list) - perf_one) > 0.2:
                            all_test_instance_perf_list.append(perf_one)
                            perf_change_zonghe_list.append(perf_one)
                            RCIW_zonghe_list.append(rciw_one)
                        else:
                            continue
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
                dict_pd["num_subscript"].append(num_subscript)
                dict_pd["dim_subscript"].append(dim_subscript)
                dict_pd["is_value_const"].append(is_value_const)
                dict_pd["is_lower_1"].append(is_lower_0)
                dict_pd["is_upper_len"].append(is_upper_len)
                dict_pd["is_step_1"].append(is_step_1)

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
        print("number of code: ", file_name, count_each_code)


    # perf_change_zonghe_list = []
    # RCIW_zonghe_list = []
    # perf_change_zonghe_left_list = []
    # perf_change_zonghe_right_list = []
    # for i, e in enumerate(dict_pd['RCIW_rm_outlier']):
    #     if dict_pd['RCIW'][i] > e:
    #         perf_change_zonghe_list.append(dict_pd['perf_change_rm_outlier'][i])
    #         RCIW_zonghe_list.append(e)
    #         perf_change_zonghe_left_list.append(dict_pd["perf_change_left_rm_outlier"][i])
    #         perf_change_zonghe_right_list.append(dict_pd["perf_change_right_rm_outlier"][i])
    #
    #     else:
    #         perf_change_zonghe_list.append(dict_pd['perf_change'][i])
    #         RCIW_zonghe_list.append(dict_pd['RCIW'][i])
    #         perf_change_zonghe_left_list.append(dict_pd["perf_change_left"][i])
    #         perf_change_zonghe_right_list.append(dict_pd["perf_change_right"][i])

    dict_pd["perf_change_zonghe"] = perf_change_zonghe_list
    dict_pd["RCIW_zonghe"] = RCIW_zonghe_list
    # dict_pd["perf_change_right_zonghe"] = perf_change_zonghe_right_list
    # dict_pd["perf_change_left_zonghe"] = perf_change_zonghe_left_list
    dict_pd["perf_change"] = perf_change_zonghe_list
    dict_pd["RCIW"] = RCIW_zonghe_list

    dataMain = pd.DataFrame(data=dict_pd, columns=['num_subscript',
        "is_value_const", 'is_lower_1', 'is_upper_len',
        'is_step_1'])
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
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_call_star_single_3_simplify_len/a_call_star_single_iter_invoca_add_perf_change_new_merge_remove_outlier_2_new/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_call_star_single_4_simplify_len_again_2/a_call_star_single_iter_invoca_add_perf_change_new_merge_remove_outlier_2_new/"

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
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_call_star_single_3_simplify_len/a_call_star_single_iter_invoca_add_perf_change_new_merge_2_new/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_call_star_single_4_simplify_len_again_2/a_call_star_single_iter_invoca_add_perf_change_new_merge_2_new/"

    file_html_dir=util.data_root_mv + "performance/a_call_star_single_2/"
    save_code_info_dir_len = util.data_root_mv + "performance/a_call_star_single_2_add_size/a_call_star_iter_invoca_2/"

    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    # csv_feature_file_name_corr= util.data_root_mv + "lab_performance/chain_compare_benchmarks_new/csv/train_data_chain_compare_new.csv"
    # dict_pd=get_features_add_interval_remove_redundant(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)


    csv_perf_change_dir = util.data_root_mv + "performance/a_call_star_single_2/csv/"
    csv_perf_change_dir = util.data_root_mv + "performance/a_call_star_single_3_simplify_len/csv/"
    csv_perf_change_dir = util.data_root_mv + "performance/a_call_star_single_4_simplify_len_again_2/csv/"

    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    csv_feature_file_name_corr= csv_perf_change_dir+"train_data_call_star.csv"
    # csv_feature_file_name_corr= csv_perf_change_dir+"train_data_call_star_remove_redundant.csv"

    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)

    print("number of dataset: ", len(dataMain["file_html"]))

    df_sample = dataMain.sample(n=119, random_state=2022)
    # df_sample.to_csv(csv_perf_change_dir + "sample_call_star_perf.csv", index=False)

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





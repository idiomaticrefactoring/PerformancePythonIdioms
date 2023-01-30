import sys,ast,os,csv,time,traceback,copy,random
import pandas as pd
from scipy.special import kl_div
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance_variability_analyze/")
sys.path.append(code_dir+"test_case/")
import util,configure_pro_envir_util
import thinkstats2
from code_info import CodeInfo
import numpy as np
import math
import ast_performance_util
from scipy import stats
RANGE_OUTLIER_FACTOR=1.5
DIVERGENCE_NUMBER_OF_POINTS=100
'''
get_XX_single_stable_fork 是只是单独看对应metrics的值的大小，不是看metrics的前后变化大小
get_XX_stable_fork 是看metrics的前后变化大小
'''
# def get_variablity_single_stable_fork(cov_list,threshold=0.02,window=1):
#     for ind,e in enumerate(cov_list[:-window]):
#         diff_cov=max(cov_list[ind:ind+window+1])
#         if diff_cov<threshold:
#             return ind+window+1,cov_list[:ind+window+1]
#     return None, None
def filter_outlier_2(valid_time_list,factor=1.5):
    data = [ee for e in valid_time_list for ee in e]

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    max_data = q3 + factor * iqr
    min_data = q1 - factor * iqr
    filter_time_list = [e for e in data if max_data > e >min_data]
    # print("num of outliers: ",len(data),len(data)-len(filter_time_list),(len(data)-len(filter_time_list))/len(data))

    return filter_time_list
def filter_outlier(valid_time_list):
    flatten_time_list = [ee for e in valid_time_list for ee in e]
    median = np.median(flatten_time_list)
    mad = stats.median_abs_deviation(flatten_time_list)
    filter_time_list = [e for e in flatten_time_list if median + 3 * mad > e > median - 3 * mad]
    print("num of outliers: ",len(flatten_time_list),len(flatten_time_list)-len(filter_time_list),(len(flatten_time_list)-len(filter_time_list))/len(flatten_time_list))
    return filter_time_list
def get_ci_perf_change_dict_merge_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf":[], "instance":[],"code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [], 'RCIW_rm_outlier': []

    }
    file_name_list=set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        print("file_name: ",file_name)
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ",save_code_info_dir_add_performance_change,file_name_no_suffix)
            continue
        try:
            lab_code_info_remove_outlier = util.load_pkl(save_code_info_dir_add_performance_change_remove_outlier,
                                                     file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ",save_code_info_dir_add_performance_change_remove_outlier,file_name_no_suffix)
            continue
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        perf_info_dict = lab_code_info.perf_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:

        for ind_tm,test_me in enumerate(perf_info_dict):

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
                print("perf_info: ", file_name, test_me, perf_info)
                print("perf_info: ", file_name, test_me, perf_info, perf_info)
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
    print("len of file and test methods: ",len(file_name_list),len(test_me_list))
    return dict_pd

def get_node_kind(node):
    if isinstance(node,ast.Subscript):
        return "Subscript"
    elif isinstance(node,ast.Call):
        return "Call"
    elif isinstance(node,ast.Attribute):
        return "Attribute"
    elif isinstance(node,ast.BinOp):
        return "BinOP"
    elif isinstance(node,ast.UnaryOp):
        return "UnaryOp"
    elif isinstance(node,ast.Compare):
        return "Compare"
    else:
        return "Other"

def get_ci_perf_change_dict_add_num_ele_two_dirs_improve(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], "num_ele":[],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [], 'RCIW_rm_outlier': []

    }
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        if file_name=="neat.graphs.feed_forward_layers_6.pkl":
            continue
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ",save_code_info_dir_add_performance_change,file_name_no_suffix)
            continue
        try:
            lab_code_info_remove_outlier = util.load_pkl(save_code_info_dir_add_performance_change_remove_outlier, file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ",save_code_info_dir_add_performance_change_remove_outlier,file_name_no_suffix)
            continue

        # perf_info_dict_remove_outlier= lab_code_info_remove_outlier.total_time_list_info_dict
        # total_time_list_info_dict_merge_remove_outlier=lab_code_info_remove_outlier.total_time_list_info_dict_merge
        perf_info_dict_remove_outlier=lab_code_info_remove_outlier.perf_info_dict
        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        # perf_info_dict = lab_code_info.total_time_list_info_dict
        perf_info_dict = lab_code_info.perf_info_dict
        total_time_list_info_dict_merge=lab_code_info.total_time_list_info_dict_merge

        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
                num_ele=total_time_list_info_dict_merge[test_me][instance]["num_ele"]
                perf_info = perf_info_dict[test_me][instance]
                perf_info_remove_outlier=perf_info_dict_remove_outlier[test_me][instance]
                print("perf_info: ", file_name, test_me,perf_info,perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))
                dict_pd["num_ele"].append(int(num_ele))
                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])
                dict_pd["perf_change_rm_outlier"].append(perf_info_remove_outlier[0])
                dict_pd["perf_change_left_rm_outlier"].append(perf_info_remove_outlier[1])
                dict_pd["perf_change_right_rm_outlier"].append(perf_info_remove_outlier[2])
                dict_pd["RCIW"].append((perf_info[2]-perf_info[1])/perf_info[0])
                dict_pd["RCIW_rm_outlier"].append((perf_info_remove_outlier[2]-perf_info_remove_outlier[1])/perf_info_remove_outlier[0])
    print("len of file and test methods: ",len(file_name_list),len(test_me_list))


    return dict_pd
def get_ci_perf_change_dict_add_num_ele_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], "num_ele":[],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [], 'RCIW_rm_outlier': []

    }
    file_name_list = set([])
    test_me_list = set([])
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix = file_name[:-4]
        try:
            lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ",save_code_info_dir_add_performance_change,file_name_no_suffix)
            continue
        try:
            lab_code_info_remove_outlier = util.load_pkl(save_code_info_dir_add_performance_change_remove_outlier, file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ",save_code_info_dir_add_performance_change_remove_outlier,file_name_no_suffix)
            continue

        perf_info_dict_remove_outlier= lab_code_info_remove_outlier.total_time_list_info_dict

        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        perf_info_dict = lab_code_info.total_time_list_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
                num_ele=perf_info_dict[test_me][instance]["num_ele"]
                perf_info = perf_info_dict[test_me][instance]["perf_change"]
                perf_info_remove_outlier=perf_info_dict_remove_outlier[test_me][instance]["perf_change"]
                print("perf_info: ", file_name, test_me,perf_info,perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))
                dict_pd["num_ele"].append(int(num_ele))
                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])
                dict_pd["perf_change_rm_outlier"].append(perf_info_remove_outlier[0])
                dict_pd["perf_change_left_rm_outlier"].append(perf_info_remove_outlier[1])
                dict_pd["perf_change_right_rm_outlier"].append(perf_info_remove_outlier[2])
                dict_pd["RCIW"].append((perf_info[2]-perf_info[1])/perf_info[0])
                dict_pd["RCIW_rm_outlier"].append((perf_info_remove_outlier[2]-perf_info_remove_outlier[1])/perf_info_remove_outlier[0])

    print("len of file and test methods: ",len(file_name_list),len(test_me_list))

    return dict_pd
def get_ci_perf_change_dict_add_num_ele(save_code_info_dir_add_performance_change):
    dict_pd = {
        "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], "num_ele":[],'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []

    }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        perf_info_dict = lab_code_info.total_time_list_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                num_ele=perf_info_dict[test_me][instance]["num_ele"]
                perf_info = perf_info_dict[test_me][instance]["perf_change"]
                print("perf_info: ", file_name, test_me,perf_info,perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))
                dict_pd["num_ele"].append(int(num_ele))
                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["RCIW"].append((perf_info[2]-perf_info[1])/perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])
    return dict_pd
def get_ci_perf_change_dict(save_code_info_dir_add_performance_change):
    dict_pd = {
        "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []

    }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        print("file_name: ",file_name)
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        perf_info_dict = lab_code_info.total_time_list_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                perf_info = perf_info_dict[test_me][instance]["perf_change"]
                print("perf_info: ", file_name, test_me,perf_info,perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))

                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["RCIW"].append((perf_info[2]-perf_info[1])/perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])
    return dict_pd
def get_ci_perf_change_dict_merge(save_code_info_dir_add_performance_change):
    dict_pd = {
        "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []

    }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        print("file_name: ",file_name)
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        perf_info_dict = lab_code_info.perf_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                perf_info = perf_info_dict[test_me][instance]
                print("perf_info: ", file_name, test_me,perf_info,perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))

                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["RCIW"].append((perf_info[2]-perf_info[1])/perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])
    return dict_pd
def save_perf_change(file_name,merge,bench_time_info_dir,save_code_info_dir_add_performance_change,invo=50):

    file_name_no_suffix = file_name[:-4]
    lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
    lab_code_info: CodeInfo

    # print("total_time_list_info_dict: ",total_time_list_info_dict)
    # for invo in invo_list:
    lab_code_info.get_performance_improve_info(total_time_list_info_dict=dict(), invocations=invo, steps=100,merge=merge)
    # print("performance change: ",lab_code_info.total_time_list_info_dict)
    util.save_pkl(save_code_info_dir_add_performance_change + str(invo) + "/", file_name_no_suffix, lab_code_info)
    print("save ",save_code_info_dir_add_performance_change + str(invo) + "/", file_name_no_suffix, "successfully")
    pass

def save_csv_perf_change(save_code_info_dir_add_performance_change,csv_perf_change_dir,csv_file_name="csv_perf_change_result.csv"):
    dict_pd={
        "file_html":[],"test_me_inf":[], "code_str":[],'perf_change':[],'RCIW':[],'perf_change_left':[],'perf_change_right':[]

    }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix=file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        lab_code_info: CodeInfo
        file_html=lab_code_info.file_html
        code_str=lab_code_info.get_code_str()
        perf_info_dict=lab_code_info.perf_info_dict
        print("file_name: ",file_name,perf_info_dict)
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                perf_info=perf_info_dict[test_me][instance]
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["RCIW"].append(perf_info[3])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])

    dataMain = pd.DataFrame(data=dict_pd)
    # print(">>>>>>drop same features: ", dataMain.keys())
        # print(dataMain.to_dict())
    dataMain.to_csv(csv_perf_change_dir+csv_file_name, index=False)
def get_cov_single_stable_fork(cov_list,threshold=0.02,window=1):
    for ind,e in enumerate(cov_list[:-window]):
        diff_cov=max(cov_list[ind:ind+window+1])
        if diff_cov<threshold:
            return ind+window+1,cov_list[:ind+window+1]
    return None,None
def get_kld_single_stable_fork(kld_list,threshold=0.9,window=1):
    for ind,e in enumerate(kld_list[:-window]):
        diff_cov=min(kld_list[ind:ind+window+1])
        if diff_cov>threshold:
            return ind+window+1,kld_list[:ind+window+1]
    return None, None
def get_ci_single_stable_fork(kld_list,threshold=0.03,window=1):
    for ind,e in enumerate(kld_list[:-window]):
        diff_cov=max(kld_list[ind:ind+window+1])
        if diff_cov<threshold:
            return ind+window+1,kld_list[ind+window]
    return None, None
def get_diff_variability_stable_fork(stop_metric_list,threshold=0.02,window=1):
    for ind, e in enumerate(stop_metric_list[:-window]):
        diff_cov = max(stop_metric_list[ind:ind + window + 1]) - min(stop_metric_list[ind:ind + window + 1])
        if diff_cov < threshold:
            return ind + window + 1, stop_metric_list[:ind + window + 1]
    return None, None
def get_cov_stable_fork(cov_list,threshold=0.02,window=1):
    for ind,e in enumerate(cov_list[:-window]):
        diff_cov=max(cov_list[ind:ind+window+1])-min(cov_list[ind:ind+window+1])
        if diff_cov<threshold:
            return ind+window+1,cov_list[:ind+window+1]
    return None, None
def get_kld_stable_fork(kld_list,threshold=0.02,window=1):
    for ind,e in enumerate(kld_list[:-window]):
        diff_cov=max(kld_list[ind:ind+window+1])-min(kld_list[ind:ind+window+1])
        if diff_cov<threshold:
            return ind+window+1,kld_list[:ind+window+1]
    return None, None
def get_ci_stable_fork(kld_list,threshold=0.02,window=1):
    for ind,e in enumerate(kld_list[:-window]):
        diff_cov=max(kld_list[ind:ind+window+1])-min(kld_list[ind:ind+window+1])
        if diff_cov<threshold:
            return ind+window+1,kld_list[ind+window]
    return None, None
# 这个是看每一次fork后置信区间的距离越来越小
def get_ci_stable_fork(kld_list,threshold=0.02,window=1):
    for ind,e in enumerate(kld_list[:-window]):
        diff_cov=max(kld_list[ind:ind+window+1])-min(kld_list[ind:ind+window+1])
        if diff_cov<threshold:
            return ind+window+1,kld_list[:ind+window+1]
    return None, None
def get_ci_diff(before,after):

    mean_list = [np.mean(e) for e in before]  # steps次的mean
    mean_after_list = [np.mean(e) for e in after]  # steps次的mean
    mean_diff_list = [abs(e - mean_after_list[ind]) / mean_after_list[ind] for ind, e in
                      enumerate(mean_list)]  # steps次的mean diff
    left, right = np.percentile(mean_diff_list, [2.5, 97.5])

    return right-left
def get_ci_diff_list(all_bootstrap_time_list):
    ci_diff_list = []
    for ind, one_invo_bootstrap_time_list in enumerate(all_bootstrap_time_list[:-1]):
        # one_invo_bootstrap_time_list 里存放这steps次的bootstrap重复采样
        diff = get_ci_diff(one_invo_bootstrap_time_list, all_bootstrap_time_list[ind + 1])
        '''
        mean_list=[np.mean(e) for e in one_invo_bootstrap_time_list]#steps次的mean
        mean_after_list = [np.mean(e) for e in all_bootstrap_time_list[ind+1]]#steps次的mean
        mean_diff_list=[abs(e-mean_after_list[ind])/mean_after_list[ind] for ind,e in enumerate(mean_list)]#steps次的mean diff
        left, right = np.percentile(mean_diff_list, [2.5, 97.5])
        '''
        ci_diff_list.append(diff)

    return ci_diff_list
# 这个是看diff的置信区间的距离越来越小
def get_ci_diff_stable_fork(ci_diff_list,threshold=0.02,window=1):
    # ci_diff_list=[]
    # for ind, one_invo_bootstrap_time_list in enumerate(all_bootstrap_time_list[:-1]):
    #     #one_invo_bootstrap_time_list 里存放这steps次的bootstrap重复采样
    #     diff=get_ci_diff(one_invo_bootstrap_time_list, all_bootstrap_time_list[ind+1])
    #     '''
    #     mean_list=[np.mean(e) for e in one_invo_bootstrap_time_list]#steps次的mean
    #     mean_after_list = [np.mean(e) for e in all_bootstrap_time_list[ind+1]]#steps次的mean
    #     mean_diff_list=[abs(e-mean_after_list[ind])/mean_after_list[ind] for ind,e in enumerate(mean_list)]#steps次的mean diff
    #     left, right = np.percentile(mean_diff_list, [2.5, 97.5])
    #     '''
    #     ci_diff_list.append(diff)
    for ind,e in enumerate(ci_diff_list[:-window]):
        diff_cov = max(ci_diff_list[ind:ind + window + 1]) - min(ci_diff_list[ind:ind + window + 1])
        if diff_cov < threshold:
            return ind + window + 1, ci_diff_list[:ind + window+1]

def kl_divergence(p, q,width=1):
    intersection = False
    kl = 0.0

    for i in range(len(p)):
        if p[i] != 0.0 and q[i] != 0.0:
            intersection = True
            try:
                kl += p[i] * math.log(p[i] / q[i]) * width
            except:
                continue

    if intersection:
        return kl
    return  math.inf

    # return np.sum(np.where(p != 0 and q != 0, p * np.log(p / q)*width, 0))
def get_max_min(data):
    # q1 = np.percentile(data, 25)
    # q3 = np.percentile(data, 75)
    # iqr = q3 - q1
    # max_data = q3 + RANGE_OUTLIER_FACTOR * iqr
    # min_data = q1 - RANGE_OUTLIER_FACTOR * iqr
    #

    max_data, min_data=np.max(data),np.min(data)
    if (min_data < 0):
        min_data = 0.0
    return max_data,min_data
def get_max_min_outlier(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    max_data = q3 + RANGE_OUTLIER_FACTOR * iqr
    min_data = q1 - RANGE_OUTLIER_FACTOR * iqr

    if (min_data < 0):
        min_data = 0.0
    # max_data, min_data=np.max(data),np.min(data)
    return max_data,min_data
'''
reimplmentation of Java version
https://github.com/sealuzh/jmh/blob/d2c4f7998c16baf322b0dbf0509e8e5250ed6380/jmh-core/src/main/java/org/openjdk/jmh/reconfigure/statistics/evaluation/DivergenceEvaluation.java
'''
def get_kld_x_y(before,after,remove_outlier=1):
    if remove_outlier:
        max_before, min_before = get_max_min_outlier(before)
        max_after, min_after = get_max_min_outlier(after)
    else:
        max_before,min_before=get_max_min(before)
        max_after,min_after=get_max_min(after)
    max_time=max(max_before,max_after)
    min_time = min(min_before, min_after)
    # print("max_time,min_time are: ",max_time,min_time)
    if max_time==min_time:
        return 1.0
    step = (max_time - min_time) / (DIVERGENCE_NUMBER_OF_POINTS - 1)
    # print("step is: ", step)
    y=[]
    for i in range(DIVERGENCE_NUMBER_OF_POINTS):
        y.append(min_time + i * step)
    y=np.array(y)
    #https://greenteapress.com/thinkstats2/html/thinkstats2007.html
    from sklearn.neighbors import KernelDensity
    #https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html
    # instantiate and fit the KDE model
    pdfBefore=thinkstats2.EstimatedPdf(before).Density(y)
    pdfAfter=thinkstats2.EstimatedPdf(after).Density(y)
    '''
    kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
    kde.fit(before[:, None])

    # score_samples returns the log of the probability density
    pdfBefore = kde.score_samples(y[:, None])
    kde.fit(after[:, None])
    pdfAfter = kde.score_samples(y[:, None])
    '''
    from scipy.special import rel_entr

    # print("pdfBefore,pdfAfter: ", pdfBefore, pdfAfter)
    kldBefore = kl_divergence(pdfBefore, pdfAfter,step)#pdfAfter
    kldAfter = kl_divergence(pdfAfter,pdfBefore,step )#kl_divergence(pdfAfter, pdfBefore,step)#sum(rel_entr(pdfBefore, pdfAfter))#
    # print("kldBefore,kldAfter: ",kldBefore,kldAfter)
    return (2.0**(-kldBefore)) * (2.0**(-kldAfter))

def compute_probs(data, n=10):
    h, e = np.histogram(data, n)
    p = h / data.shape[0]
    return e, p


def support_intersection(p, q):
    sup_int = (
        list(
            filter(
                lambda x: (x[0] != 0) & (x[1] != 0), zip(p, q)
            )
        )
    )
    return sup_int


def get_probs(list_of_tuples):
    p = np.array([p[0] for p in list_of_tuples])
    q = np.array([p[1] for p in list_of_tuples])
    return p, q




def js_divergence(p, q):
    m = (1. / 2.) * (p + q)
    return (1. / 2.) * kl_divergence(p, m) + (1. / 2.) * kl_divergence(q, m)
def ecdf(x):
    x = np.sort(x)
    u, c = np.unique(x, return_counts=True)
    n = len(x)
    y = (np.cumsum(c) - 0.5)/n
    def interpolate_(x_):
        yinterp = np.interp(x_, u, y, left=0.0, right=1.0)
        return yinterp
    return interpolate_

def cumulative_kl(x,y,fraction=0.5):
    dx = np.diff(np.sort(np.unique(x)))
    dy = np.diff(np.sort(np.unique(y)))
    ex = np.min(dx)
    ey = np.min(dy)
    e = np.min([ex,ey])*fraction
    n = len(x)
    P = ecdf(x)
    Q = ecdf(y)
    KL = (1./n)*np.sum(np.log((P(x) - P(x-e))/(Q(x) - Q(x-e))))
    return KL

def compute_kl_divergence(train_sample, test_sample, n_bins=10):
    """
    Computes the KL Divergence using the support
    intersection between two different samples
    """
    e, p = compute_probs(train_sample, n=n_bins)
    _, q = compute_probs(test_sample, n=e)

    list_of_tuples = support_intersection(p, q)
    p, q = get_probs(list_of_tuples)

    return kl_divergence(p, q)


def compute_js_divergence(train_sample, test_sample, n_bins=10):
    """
    Computes the JS Divergence using the support
    intersection between two different samples
    """
    e, p = compute_probs(train_sample, n=n_bins)
    _, q = compute_probs(test_sample, n=e)

    list_of_tuples = support_intersection(p, q)
    p, q = get_probs(list_of_tuples)

    return js_divergence(p, q)
def compute_cov(data):
    return   np.std(data) / np.mean(data)
def compute_ci(all_boot_time_list):
    prf_change_list=[]
    for ind_step, boot_time_list in enumerate(all_boot_time_list):
        per_change_mean=np.mean(boot_time_list)
        prf_change_list.append(per_change_mean)
    left, right = np.percentile(prf_change_list, [2.5, 97.5])

    return   left,right
def get_time_list_within_cov(time_list,window):
    valid_time_list = []
    # for ind_t, e in enumerate(time_list):
    for i in range(len(time_list) - window + 1):
            cov = np.std(time_list[i:i + window]) / np.mean(time_list[i:i + window])
            if cov <= 0.02:
                valid_time_list=copy.deepcopy(time_list[i:i + window])
                break
    return valid_time_list
def whether_cov(time_list,window):

    for i in range(len(time_list) - window + 1):
            cov = np.std(time_list[i:i + window]) / np.mean(time_list[i:i + window])
            # print("cov: ",cov)
            if cov <= 0.02:
                return 1
    return 0

def get_var(content,var_list):
    var_dict=dict()

    for line in content.split("\n"):
        if line.startswith("len: "):
            var_list.append(var_dict)
            var_dict = dict()
        if line.startswith("type: "):
            num=line.split(": ")[1:]
            # if num[0].strip() in var_dict:
            #     var_list.append(var_dict)
            #     var_dict=dict()
            var_dict[num[0].strip()]=num[1].strip()


    var_list.append(var_dict)
                # return str(num)
    # return var_dict
def get_var_two_dimen(content):
    number_list=[]
    count_test_method=0
    a = []
    for line in content.split("\n"):
        if line.startswith(">>>>>>>>Come tested method zejun"):
            if a:
                number_list.append(a)
                a=[]
            count_test_method+=1
        if line.startswith("type: "):
            num = line.split(": ")[1:]
        # if line.startswith("len: "):
        #     num=line.split(":")[-1].strip()
            a.append([num[0].strip(), num[1].strip()])
            # if num.isdigit():
            #     a.append(str(num))
                # number_list.append(a)
                # return str(num)
    if a:# and a not in time_list:
        number_list.append(a)
    return number_list
def get_size(content):
    number_list=[]
    for line in content.split("\n"):
        if line.startswith("mymysizeof: "):
            num=line.split("mymysizeof:")[-1].strip()
            number_list.append(str(num))
                # return str(num)
    return number_list
def get_time_list(run_test_result_new):
    time_list=[]
    ind=len("*********zejun test total time**************")
    for e in run_test_result_new.split("\n"):
        if e.startswith("*********zejun test total time**************"):
            time_list.append(e[ind:].strip())
    return time_list
def get_pythonic_time_list(run_test_result_new):
    time_list=[]
    ind=len("*********zejun test total time pythonic**************")
    for e in run_test_result_new.split("\n"):
        if e.startswith("*********zejun test total time pythonic**************"):
            time_list.append(e[ind:].strip())
    return time_list
def get_num_add_ele(content):
    number_list=[]
    for line in content.split("\n"):
        if line.startswith("len: "):
            num=line.split(":")[-1].strip()
            if num.isdigit():
                number_list.append(str(num))
                # return str(num)
    return number_list
def get_num_add_ele_two_dimen(content):
    number_list=[]
    count_test_method=0
    a = []
    for line in content.split("\n"):
        if line.startswith(">>>>>>>>Come tested method zejun"):
            if a:
                number_list.append(a)
                a=[]
            count_test_method+=1
        if line.startswith("len: "):
            num=line.split(":")[-1].strip()
            if num.isdigit():
                a.append(str(num))
                # number_list.append(a)
                # return str(num)
    if a:# and a not in time_list:
        number_list.append(a)
    return number_list
def get_isBreak_two_dimen(content):
    number_list=[]
    count_test_method=0
    a = []
    for line in content.split("\n"):
        if line.startswith(">>>>>>>>Come tested method zejun"):
            if a:
                number_list.append(a)
                a=[]
            count_test_method+=1
        if line.startswith("isBreak: "):
            num=line.split(":")[-1].strip()
            if num.isdigit():
                a.append(str(num))
                # number_list.append(a)
                # return str(num)
    if a:# and a not in time_list:
        number_list.append(a)
    return number_list
def get_isTrue_two_dimen(content):
    number_list=[]
    count_test_method=0
    a = []
    for line in content.split("\n"):
        if line.startswith(">>>>>>>>Come tested method zejun"):
            if a:
                number_list.append(a)
                a=[]
            count_test_method+=1
        if line.startswith("isTrue: "):
            num=line.split(":")[-1].strip()
            if num.isdigit():
                a.append(str(num))
                # number_list.append(a)
                # return str(num)
    if a:# and a not in time_list:
        number_list.append(a)
    return number_list
def get_pythonic_time_list_two_dimen(run_test_result_new):
    time_list=[]
    count_test_method=0
    ind=len("*********zejun test total time pythonic**************")
    a = []
    for e in run_test_result_new.split("\n"):
        # print("each line of run_test_result_new: ",e)
        if e.startswith(">>>>>>>>Come tested method zejun"):
            if a:
                time_list.append(a)
                a=[]
            count_test_method+=1

        if e.startswith("*********zejun test total time pythonic**************"):
            a.append(e[ind:].strip())
            # time_list.append(e[ind:].strip())
    if a:# and a not in time_list:
        time_list.append(a)
    print(">>>>>>>>>>count_test_method: ",count_test_method)
    return time_list
def get_time_list_two_dimen(run_test_result_new):
    time_list=[]
    count_test_method = 0
    ind=len("*********zejun test total time**************")
    a = []
    for e in run_test_result_new.split("\n"):
        if e.startswith(">>>>>>>>Come tested method zejun"):
            if a:
                time_list.append(a)
                a = []
            count_test_method+=1
        if e.startswith("*********zejun test total time**************"):
            a.append(e[ind:].strip())
            # time_list.append(e[ind:].strip())
    if a:# and a not in time_list:
        time_list.append(a)
    print(">>>>>>>>>>count_test_method: ", count_test_method)
    return time_list
def get_time_list_two_dimen(run_test_result_new):
    time_list=[]
    count_test_method = 0
    ind=len("*********zejun test total time**************")
    a = []
    for e in run_test_result_new.split("\n"):
        if e.startswith(">>>>>>>>Come tested method zejun"):
            if a:
                time_list.append(a)
                a = []
            count_test_method+=1
        if e.startswith("*********zejun test total time**************"):
            a.append(e[ind:].strip())
            # time_list.append(e[ind:].strip())
    if a:# and a not in time_list:
        time_list.append(a)
    print(">>>>>>>>>>count_test_method: ", count_test_method)
    return time_list

def backup_content(repo_path,file_html):
    real_file_html = file_html.replace("//", "/")
    rela_path = real_file_html.split("/")[6:]
    old_path = repo_path + "/".join(rela_path)
    rela_path[-1] = "".join([rela_path[-1][:-3], util.copy_file_suffix, ".py"])
    rela_path = "/".join(rela_path)
    print("copy_file_path: ", repo_path + rela_path)
    old_content = util.load_file_path(old_path)
    util.save_file_path(repo_path + rela_path, old_content)  # copy 一份原来的文件防止失去
    print(">>>>>>>>>>>>> backup old files succeeded into ", repo_path + rela_path)


def backup_pythonic_content(repo_path,file_html, new_content):
    real_file_html = file_html.replace("//", "/")
    rela_path = real_file_html.split("/")[6:]
    rela_path_test_pythonic_file_name = "".join(
        [rela_path[-1][:-3], util.copy_file_suffix + "_test_insert_timeit_pythonic", ".py"])
    rela_path[-1] = "".join([rela_path[-1][:-3], util.copy_file_suffix, ".py"])
    rela_path_test_pythonic = "/".join(rela_path[:-1]) + "/" + rela_path_test_pythonic_file_name

    util.save_file_path(repo_path + rela_path_test_pythonic,
                        new_content)
    print(">>>>>>>>>>>>> backup pythonic code succeeded into ", repo_path + rela_path_test_pythonic)


def backup_time_content(repo_path,file_html, new_content):
    real_file_html = file_html.replace("//", "/")
    rela_path = real_file_html.split("/")[6:]
    rela_path_test_file_name = "".join(
        [rela_path[-1][:-3], util.copy_file_suffix + "_test_insert_timeit", ".py"])
    rela_path[-1] = "".join([rela_path[-1][:-3], util.copy_file_suffix, ".py"])
    rela_path_test = "/".join(rela_path[:-1]) + "/" + rela_path_test_file_name
    util.save_file_path(repo_path + rela_path_test, new_content)
    print(">>>>>>>>>>>>> backup of insert time code succeeded into ", repo_path + rela_path_test)


def make_new_test_file(repo_path, test_html, cl, me, iterations=10):
    relative_test_file = "/".join(test_html.replace("//", "/").split("/")[6:])
    test_full_file_path = repo_path + relative_test_file
    copy_test_full_file_path = "".join([test_full_file_path[:-3], util.copy_file_suffix, ".py"])
    new_test_html = "".join([test_html[:-3], util.copy_file_suffix, ".py"])
    print("test_html: ", copy_test_full_file_path, test_html, new_test_html, cl, me,
          test_full_file_path)

    old_content = util.load_file_path(test_full_file_path)
    # test_code=util.load_file_path(copy_test_full_file_path)
    # print("test_code: ",test_code)
    file_tree = ast.parse(old_content)
    ana_py = ast_performance_util.Fun_Analyzer(me, iterations)
    file_tree = ana_py.visit(file_tree)
    new_test_code = ast.unparse(file_tree)
    # print("test code of test method: ", file_tree, ana_py.flag)
    # print(ast.unparse(file_tree))
    util.save_file_path(copy_test_full_file_path, new_test_code)  # copy 一份原来的文件防止失去
    copy_test_full_file_path = "".join([test_full_file_path[:-3], util.copy_file_suffix, ".py"])
    new_test_html = "".join([test_html[:-3], util.copy_file_suffix, ".py"])
    # print("test_html: ", copy_test_full_file_path, test_html, new_test_html, cl, me,
    #       test_full_file_path)
    return new_test_html


def code_test_get_time(repo_path, old_path, old_content, test_me_inf_list, is_pythonic_timeflag=0, is_own_config=0,is_new_test_html=1):
    all_test_case_time_list = dict()
    try:
        for test_html, each_rela_path, cl, me in test_me_inf_list:

            fun_list = ["::".join([cl, me]) if cl else me]
            if is_new_test_html:
                new_test_html = make_new_test_file(repo_path, test_html, cl, me)
            else:
                new_test_html=test_html
            if not is_own_config:
                run_test_result_new = configure_pro_envir_util.run_test_file_capture_output(new_test_html, repo_path,
                                                                                            fun_list=fun_list,
                                                                                            export_python=True)
            else:
                run_test_result_new = configure_pro_envir_util.run_test_file_capture_output(new_test_html, repo_path,
                                                                                            ven_name="venv_zejun_config",
                                                                                            fun_list=fun_list,
                                                                                     export_python=False)
            print("test_html: ", new_test_html)
            print(">>>>>>>>>>run_test_result_new: ", run_test_result_new)
            if is_pythonic_timeflag:
                time_list = get_pythonic_time_list(run_test_result_new)
            else:
                time_list = get_time_list(run_test_result_new)
            all_test_case_time_list[(test_html, each_rela_path, cl, me)] = time_list
            # print(">>>>>>>>>>run_test_result_new: ", run_test_result_new)
            # print("time_list: ", time_list)
            '''
            if time_list:
                all_test_case_time_list[(test_html, each_rela_path, cl, me)]=time_list            
            '''


        else:
            flag_success = 1
            # '''
            util.save_file_path(old_path, old_content)

            print("****************we save the old content to original file: ", old_path)
            # '''
    except:
        # '''
        print("****************CODE RUN OCCUR ERRORS")
        util.save_file_path(old_path, old_content)
        print("****************we save the old content to original file: ", old_path)

        # '''
        traceback.print_exc()
    # print(f"{loop_num} loops, total time: {end-start}")
    return all_test_case_time_list
def bootstrap(x,x_new):
    if isinstance(x, list):
        new_index=random.choices([i for i in range(len(x))],k=len(x))
        # print("new_index: ",new_index)
        for i,e in enumerate(x):
                x_new[i]=copy.deepcopy(x[new_index[i]])
                # print(x_new)
                bootstrap(x[new_index[i]],x_new[i])
def num_bootstrap(x,steps=1000):
    all_x_new=[]

    for i in range(steps):
        x_new = copy.deepcopy(x)
        bootstrap(x, x_new)
        all_x_new.append(x_new)
    return all_x_new
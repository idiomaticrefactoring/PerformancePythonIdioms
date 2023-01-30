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
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_list_comprehension
import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util,util_perf
from lab_code_info import LabCodeInfo
def get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_perf_change = lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change)
    # dict_pd=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change_remove_outlier)

    # '''
    dict_pd_remove_outlier = lab_performance_util.get_ci_perf_change_dict(
        save_code_info_dir_add_performance_change_remove_outlier)
    for key in dict_pd_remove_outlier:
        if key not in ["file_html", "code_str"]:
            dict_perf_change[key + "_rm_outlier"] = []
    for file_html in dict_perf_change["file_html"]:
        index = dict_pd_remove_outlier["file_html"].index(file_html)
        for key in dict_pd_remove_outlier:
            if key not in ["file_html", "code_str"]:
                dict_perf_change[key + "_rm_outlier"].append(dict_pd_remove_outlier[key][index])
    # '''
    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
    perf_change_zonghe_left_list = []
    perf_change_zonghe_right_list = []
    for i, e in enumerate(dict_perf_change['RCIW_rm_outlier']):
        if dict_perf_change['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_perf_change['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
            perf_change_zonghe_left_list.append(dict_perf_change["perf_change_left_rm_outlier"][i])
            perf_change_zonghe_right_list.append(dict_perf_change["perf_change_right_rm_outlier"][i])

        else:
            perf_change_zonghe_list.append(dict_perf_change['perf_change'][i])
            RCIW_zonghe_list.append(dict_perf_change['RCIW'][i])
            perf_change_zonghe_left_list.append(dict_perf_change["perf_change_left"][i])
            perf_change_zonghe_right_list.append(dict_perf_change["perf_change_right"][i])

    dict_perf_change["perf_change_zonghe"] = perf_change_zonghe_list
    dict_perf_change["RCIW_zonghe"] = RCIW_zonghe_list
    dict_perf_change["perf_change_right_zonghe"] = perf_change_zonghe_right_list
    dict_perf_change["perf_change_left_zonghe"] = perf_change_zonghe_left_list

    dict_pd = {"file_html":[], "code_str":[],"RCIW":[],"perf_change_right":[],"perf_change_left":[],"perf_change":[],"kind":[],"num_ele":[],'num_subscript': [],
               "is_value_const":[],'is_lower_0': [], 'is_upper_len': [],
               'is_step_1': [],'context': [],"is_total_data":[]}
    dict_pd["file_html"] = dict_perf_change["file_html"]
    dict_pd["code_str"] = dict_perf_change["code_str"]
    # print(dict_perf_change["code_str"])
    dict_pd["RCIW"]=RCIW_zonghe_list
    dict_pd["perf_change_right"]=perf_change_zonghe_right_list
    dict_pd["perf_change_left"] = perf_change_zonghe_left_list
    dict_pd["perf_change"] = perf_change_zonghe_list
    # '''
    # dict_pd["file_html"]=dict_perf_change["file_html"]
    # dict_pd["code_str"] = dict_perf_change["code_str"]
    for ind, file_name in enumerate(dict_perf_change["file_html"]):
        # print(file_name,dict_pd["code_str"][ind])
        file_name_no_suffix = file_name[:-4]
        data_size = int(file_name_no_suffix.split("_")[2])
        num_subscript = int(file_name_no_suffix.split("_")[8])

        #0_Endflag_20_num_0_lower_1_step_3_subscript_func
        dict_pd["num_ele"].append(data_size)
        dict_pd["num_subscript"].append(num_subscript)
        # if "[" in
        if "var_lower" in file_name:
            dict_pd["is_value_const"].append(0)
        else:
            dict_pd["is_value_const"].append(1)
        if "0_lower" in file_name:
            dict_pd["is_lower_0"].append(1)
        else :
            dict_pd["is_lower_0"].append(0)
        if "0_Endflag" in file_name:
            dict_pd["is_upper_len"].append(0)
        else:
            dict_pd["is_upper_len"].append(1)
        if "0_lower" in file_name and "0_Endflag" not in file_name and "1_step" in file_name:
            dict_pd["is_total_data"].append(1)
            # print("is_total_data: ",1)
        else:
            dict_pd["is_total_data"].append(0)
            # print("is_total_data: ", 0)
        if "1_step" in file_name:
            dict_pd["is_step_1"].append(1)
        else:
            dict_pd["is_step_1"].append(0)
        if "_func" in file_name:
            dict_pd["context"].append(0)
        else:
            dict_pd["context"].append(1)
        low = (dict_pd["perf_change_left"][ind])
        e=dict_pd["perf_change_right"][ind]
        if low <= 1 <= e:

            dict_pd["kind"].append("unchange")
        elif low > 1:

            dict_pd["kind"].append("improve")
        else:

            dict_pd["kind"].append("regression")
    dataMain = pd.DataFrame(data=dict_pd)
    for key in dataMain:
        feature = dataMain[key]
        # average=feature.mean()
        # std = feature.std()
        try:
            a = scipy.stats.skew(feature)
            print("skew: ", key, a)
        except:
            print(f"the key {key} cannot compute the skew")
            traceback.print_exc()
    return dict_pd
def get_reason(dataMain):
    file_html=dataMain["file_html"]
    perf_change=dataMain["perf_change"]
    # dataMain['add_byte']=[0 for i in range(dataMain["perf_change"])]
    # dataMain['remove_byte'] = [0 for i in range(dataMain["perf_change"])]
    # dataMain['replace_unique_byte'] = [0 for i in range(dataMain["perf_change"])]
    # dataMain['replace_byte'] = [0 for i in range(dataMain["perf_change"])]
    # dataMain['replace_total_byte'] = [0 for i in range(dataMain["perf_change"])]
    unique_num=0
    add_num=0
    remove_num=0
    for ind,file_name in enumerate(file_html):

        if perf_change[ind]>1:
            # dataMain['remove_byte'][ind]=1
            remove_num+=1
        else:
            # dataMain['add_byte'][ind] = 1
            add_num+=1
    sum_num=unique_num+remove_num+add_num

    print(unique_num,remove_num,add_num)
    print(unique_num/sum_num, remove_num/sum_num, add_num/sum_num)

if __name__ == '__main__':
    # bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    # total_file_list = [e[:-3] for e in os.listdir(bench_dir)]

    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3_improve/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"

    dict_pd=get_features_add_interval(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    dir_csv_feature= util.data_root_mv + "lab_performance/call_star_benchmarks/csv/"

    csv_feature_file_name_corr= util.data_root_mv + "lab_performance/call_star_benchmarks/csv/train_data_call_star.csv"
    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)
    df_sample=dataMain.sample(n=310,random_state=2022,ignore_index=True)
    get_reason(df_sample)
    df_sample.to_csv(dir_csv_feature+"sample_call_star.csv", index=False)


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
    '''
    import seaborn as sns

    tips = sns.load_dataset("tips")
    print(tips)
    ax = sns.violinplot(x="kind", y="num_subscript", data=dict_pd,
    order = ["unchange", "improve","regression"])
    plt.show()

    import numpy as np
    import matplotlib.pyplot as plt
#https://zhuanlan.zhihu.com/p/25128216
    size = 29
    x = [i+2 for i in range(size)]
    a=[0 for i in range(size)]
    b =[0 for i in range(size)]
    c =[0 for i in range(size)]
    total_size=len(dict_pd['num_subscript'])
    for ind, e in enumerate(dict_pd['num_subscript']):
        e=e-2
        # print(e)
        if dict_pd["kind"][ind] == "improve":
            a[e]+=1
        elif dict_pd["kind"][ind] == "regression":
            b[e] += 1
        else:
            c[e] += 1
    print(a,b,c)
    a=[e/total_size for e in a]
    b = [e / total_size for e in b]
    c = [e / total_size for e in c]
    # a = [ for ind,e in enumerate(dict_pd['num_subscript']) if dict_pd["kind"]=="improve"]
    # b = np.random.random(size)
    # c = np.random.random(size)

    total_width, n = 0.8, 3
    width = total_width / n
    x = np.array(x) - (total_width - width) / 2

    plt.bar(x, a, width=width, label='improve')
    plt.bar(x + width, b, width=width, label='regression')
    plt.bar(x + 2 * width, c, width=width, label='unchange')
    plt.legend()
    plt.show()
'''





import sys, ast, os, csv, time, copy
import shutil
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
import util
import lab_performance_util
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/multi_ass_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier_1 = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier_1 = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"

    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/multi_ass_benchmarks/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change_1 = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/prefined_cpus_remain_code_new_add_perf_change/"

    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/prefined_cpus_remain_code_new_add_perf_change/"

    exist_file_list=list(os.listdir(save_code_info_dir_add_performance_change_remove_outlier_1))
    count=0
    for e in os.listdir(save_code_info_dir_add_performance_change_remove_outlier):
        # print(e)
        if e not in exist_file_list:
            count+=1
            shutil.copyfile(save_code_info_dir_add_performance_change_remove_outlier+e,save_code_info_dir_add_performance_change_remove_outlier_1+e)
            # print(e)
            # break
    print("count: ",count)
    exist_file_list = list(os.listdir(save_code_info_dir_add_performance_change_1))
    count = 0
    for e in os.listdir(save_code_info_dir_add_performance_change):
        # print(e)
        if e not in exist_file_list:
            count += 1
            shutil.copyfile(save_code_info_dir_add_performance_change + e,
                            save_code_info_dir_add_performance_change_1 + e)
            # print(e)
            # break
    print("count: ", count)
    #'''
    perf_improve_dict={
        "file_html": [], "code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    }
    perf_regression_dict={
        "file_html": [], "code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    }
    perf_unchange_dict = {
        "file_html": [], "code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    }
    dict_pd=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change)
    # dict_pd=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change_remove_outlier)


    dict_pd_remove_outlier=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change_remove_outlier)
    for key in dict_pd_remove_outlier:
        if key not in ["file_html","code_str"]:
            dict_pd[key+"_rm_outlier"]=[]
    for file_html in dict_pd["file_html"]:
        index=dict_pd_remove_outlier["file_html"].index(file_html)
        for key in dict_pd_remove_outlier:
            if key not in ["file_html","code_str"]:
                dict_pd[key+"_rm_outlier"].append(dict_pd_remove_outlier[key][index])

    perf_change_list = dict_pd["perf_change"]
    RCIW_list = dict_pd["RCIW"]
    perf_change_left = dict_pd['perf_change_left']
    perf_change_right = dict_pd['perf_change_right']
    plt.boxplot(perf_change_list)
    plt.show()
    print("count,mean, median, min, max: ", len(RCIW_list), np.mean(RCIW_list),
          np.median(RCIW_list), np.min(RCIW_list), np.max(RCIW_list))
    print("count,mean, median, min, max: ", len(perf_change_list), np.mean(perf_change_list),
          np.median(perf_change_list), np.min(perf_change_list), np.max(perf_change_list))

    remain_list = []
    for ind, e_rciw in enumerate(RCIW_list):
        if e_rciw > 0.1:
            remain_list.append(dict_pd["file_html"][ind])


    perf_change_list = dict_pd["perf_change_rm_outlier"]
    RCIW_list = dict_pd["RCIW_rm_outlier"]
    perf_change_left = dict_pd['perf_change_left_rm_outlier']
    perf_change_right = dict_pd['perf_change_right_rm_outlier']
    plt.boxplot(perf_change_list)
    plt.show()
    print("count,mean, median, min, max: ", len(RCIW_list), np.mean(RCIW_list),
          np.median(RCIW_list), np.min(RCIW_list), np.max(RCIW_list))
    print("count,mean, median, min, max: ", len(perf_change_list), np.mean(perf_change_list),
          np.median(perf_change_list), np.min(perf_change_list), np.max(perf_change_list))

    perf_change_zonghe_list = []
    perf_left_change_zonghe_list = []
    perf_right_change_zonghe_list = []

    RCIW_zonghe_list = []
    for i, e in enumerate(dict_pd['RCIW_rm_outlier']):
        if dict_pd['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_pd['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
            perf_left_change_zonghe_list.append(dict_pd['perf_change_left_rm_outlier'][i])
            perf_right_change_zonghe_list.append(dict_pd['perf_change_right_rm_outlier'][i])
        else:
            perf_change_zonghe_list.append(dict_pd['perf_change'][i])
            RCIW_zonghe_list.append(dict_pd['RCIW'][i])
            perf_left_change_zonghe_list.append(dict_pd['perf_change_left'][i])
            perf_right_change_zonghe_list.append(dict_pd['perf_change_right'][i])
    plt.boxplot(perf_change_zonghe_list)
    plt.show()

    dict_pd["perf_change_zonghe"] = perf_change_zonghe_list
    dict_pd["RCIW_zonghe"] = RCIW_zonghe_list
    dict_pd["perf_left_change_zonghe"] = perf_left_change_zonghe_list
    dict_pd["perf_right_change_zonghe"] = perf_right_change_zonghe_list
    print("count,mean, median, min, max: ", len(perf_change_zonghe_list), np.mean(perf_change_zonghe_list),
          np.median(perf_change_zonghe_list), np.min(perf_change_zonghe_list), np.max(perf_change_zonghe_list))
    print("count,mean, median, min, max: ", len(RCIW_zonghe_list), np.mean(RCIW_zonghe_list),
          np.median(RCIW_zonghe_list), np.min(RCIW_zonghe_list),
          np.max(RCIW_zonghe_list))


    print(remain_list)
    print("len of file: ", len(remain_list))
    #'''
    #'''
    dataMain = pd.DataFrame(data=dict_pd)
    # print(">>>>>>drop same features: ", dataMain.keys())
    # print(dataMain.to_dict())
    file_name_list_2=[]
    for ind,e in enumerate(perf_change_zonghe_list):
        if e>3:
            file_name_list_2.append(dict_pd["file_html"][ind])
    print(len(file_name_list_2))
    print(file_name_list_2)
    csv_perf_change_dir = util.data_root_mv + "lab_performance/set_compre_benchmarks/csv/"
    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    dataMain.to_csv(csv_perf_change_dir + "set_compre_two_configure_perf_change_ci_2.csv", index=False)
    #'''
    # dataMain = pd.DataFrame(data=dict_pd)
    # # print(">>>>>>drop same features: ", dataMain.keys())
    # # print(dataMain.to_dict())
    # csv_perf_change_dir=util.data_root_mv + "lab_performance/set_compre_benchmarks/csv/"
    #
    # dataMain.to_csv(csv_perf_change_dir + "two_configure_perf_change_ci.csv", index=False)

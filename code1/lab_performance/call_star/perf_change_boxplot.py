import sys, ast, os, csv, time, copy
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
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/set_compre_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3_improve/"

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
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"
    save_code_info_dir_add_performance_change = \
        util.data_root_mv + "lab_performance/call_star_benchmarks/prefined_cpus_remain_code_new_add_perf_change_improve/"

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

    #'''
    dict_pd_remove_outlier=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change_remove_outlier)
    for key in dict_pd_remove_outlier:
        if key not in ["file_html","code_str"]:
            dict_pd[key+"_rm_outlier"]=[]
    for file_html in dict_pd["file_html"]:
        index=dict_pd_remove_outlier["file_html"].index(file_html)
        for key in dict_pd_remove_outlier:
            if key not in ["file_html","code_str"]:
                dict_pd[key+"_rm_outlier"].append(dict_pd_remove_outlier[key][index])
    #'''
    # dataMain = pd.DataFrame(data=dict_pd)
    # print(">>>>>>drop same features: ", dataMain.keys())
    # print(dataMain.to_dict())
    csv_perf_change_dir=util.data_root_mv + "lab_performance/call_star_benchmarks/csv/"
    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    # dataMain.to_csv(csv_perf_change_dir + "two_configure_perf_change_ci.csv", index=False)

    perf_change_list=dict_pd["perf_change"]
    RCIW_list=dict_pd["RCIW"]
    perf_change_left=dict_pd['perf_change_left']
    perf_change_right=dict_pd['perf_change_right']
    plt.boxplot(perf_change_list)
    plt.show()
    print("count,mean, median, min, max: ", len(RCIW_list), np.mean(RCIW_list),
          np.median(RCIW_list), np.min(RCIW_list), np.max(RCIW_list))
    print("count,mean, median, min, max: ", len(perf_change_list), np.mean(perf_change_list),
          np.median(perf_change_list), np.min(perf_change_list), np.max(perf_change_list))
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
    RCIW_zonghe_list = []
    for i, e in enumerate(dict_pd['RCIW_rm_outlier']):
        if dict_pd['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_pd['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
        else:
            perf_change_zonghe_list.append(dict_pd['perf_change'][i])
            RCIW_zonghe_list.append(dict_pd['RCIW'][i])
    large_1_zonghe = [i for i, e in enumerate(perf_change_zonghe_list) if e > 1]
    plt.boxplot(perf_change_zonghe_list)
    plt.show()
    dict_pd["perf_change_zonghe"] = perf_change_zonghe_list
    dict_pd["RCIW_zonghe"] = RCIW_zonghe_list
    print("count,mean, median, min, max: ", len(perf_change_zonghe_list), np.mean(perf_change_zonghe_list),
          np.median(perf_change_zonghe_list), np.min(perf_change_zonghe_list), np.max(perf_change_zonghe_list))
    print("count,mean, median, min, max: ", len(RCIW_zonghe_list), np.mean(RCIW_zonghe_list),
          np.median(RCIW_zonghe_list), np.min(RCIW_zonghe_list),
          np.max(RCIW_zonghe_list))
    dataMain = pd.DataFrame(data=dict_pd)
    # print(">>>>>>drop same features: ", dataMain.keys())
    # print(dataMain.to_dict())
    csv_perf_change_dir=util.data_root_mv + "lab_performance/call_star_benchmarks/csv/"

    dataMain.to_csv(csv_perf_change_dir + "two_configure_perf_change_ci.csv", index=False)

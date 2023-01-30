import sys, ast, os, csv, time, copy
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import util
import performance_util
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def get_two_method_perf_change():


    perf_improve_dict=performance_util.get_ci_perf_change_dict_add_num_ele_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    perf_improve_list=perf_improve_dict['perf_change']
if __name__ == '__main__':
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_total_data/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_set_comprehension/a_set_comprehension_iter_invoca_add_perf_change_new_merge/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_set_comprehension/a_set_comprehension_iter_invoca_add_perf_change_new_merge_2/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_set_comprehension_2/a_set_comprehension_iter_invoca_add_perf_change_new_merge_2/"

    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_remove_outlier_total_data/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_set_comprehension/a_set_comprehension_iter_invoca_add_perf_change_new_merge_remove_outlier_2/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_set_comprehension_2/a_set_comprehension_iter_invoca_add_perf_change_new_merge_remove_outlier_2/"

    # dict_pd=performance_util.get_ci_perf_change_dict_merge(save_code_info_dir_add_performance_change)
    # dict_pd=performance_util.get_ci_perf_change_dict_merge_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    dict_pd=performance_util.get_ci_perf_change_dict_add_num_ele_two_dirs_improve(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)

    # perf_improve_list=perf_improve_dict['perf_change']
    print(
        f"total number of {len(os.listdir(save_code_info_dir_add_performance_change))} files in perf_dir, {len(set(dict_pd['file_html']))}file_html,"
        f" {len(dict_pd['test_me_inf'])}, {len(set(dict_pd['test_me_inf']))} test method,"
        f" {len(dict_pd['instance'])}, {len(set(dict_pd['instance']))}test instances: ")

    perf_improve_list=dict_pd['perf_change']
    RCIW_list = dict_pd['RCIW']


    print("count,mean, median, min, max: ",len(perf_improve_list), np.mean(perf_improve_list), np.median(perf_improve_list), np.min(perf_improve_list), np.max(perf_improve_list))
    print("count,mean, median, min, max: ",len(RCIW_list), np.mean(RCIW_list), np.median(RCIW_list), np.min(RCIW_list), np.max(RCIW_list))

    plt.boxplot(perf_improve_list)
    plt.show()
    perf_improve_list = dict_pd['perf_change_rm_outlier']
    RCIW_list = dict_pd['RCIW_rm_outlier']
    print("count,mean, median, min, max: ", len(perf_improve_list), np.mean(perf_improve_list),
          np.median(perf_improve_list), np.min(perf_improve_list), np.max(perf_improve_list))
    print("count,mean, median, min, max: ", len(RCIW_list), np.mean(RCIW_list), np.median(RCIW_list), np.min(RCIW_list),
          np.max(RCIW_list))

    # print("count,mean, median, min, max: ", len(perf_regression_list), np.mean(perf_regression_list),np.median(perf_regression_list), np.min(perf_regression_list), np.max(perf_regression_list))
    plt.boxplot(perf_improve_list)
    plt.show()

    perf_change_zonghe_list = []
    RCIW_zonghe_list = []
    for i, e in enumerate(dict_pd['RCIW_rm_outlier']):
        if dict_pd['RCIW'][i] > e:
            perf_change_zonghe_list.append(dict_pd['perf_change_rm_outlier'][i])
            RCIW_zonghe_list.append(e)
        else:
            perf_change_zonghe_list.append(dict_pd['perf_change'][i])
            RCIW_zonghe_list.append(dict_pd['RCIW'][i])
    plt.boxplot(perf_change_zonghe_list)
    plt.show()

    dict_pd["perf_change_zonghe"] = perf_change_zonghe_list
    dict_pd["RCIW_zonghe"] = RCIW_zonghe_list
    print("count,mean, median, min, max: ", len(perf_change_zonghe_list), np.mean(perf_change_zonghe_list),
          np.median(perf_change_zonghe_list), np.min(perf_change_zonghe_list), np.max(perf_change_zonghe_list))
    print("count,mean, median, min, max: ", len(RCIW_zonghe_list), np.mean(RCIW_zonghe_list),
          np.median(RCIW_zonghe_list), np.min(RCIW_zonghe_list),
          np.max(RCIW_zonghe_list))

    csv_perf_change_dir=util.data_root_mv + "performance/a_set_comprehension/csv/"
    csv_perf_change_dir=util.data_root_mv + "performance/a_set_comprehension_2/csv/"

    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    # csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_2_50_invocations/"
    prefix_csv_perf_change="remove_outlier_3factor_"
    # prefix_csv_perf_change = "remove_outlier_1.5factor_"
    # prefix_csv_perf_change = "2nd_invo_remove_outlier_3_factor_"
    # prefix_csv_perf_change = "2nd_invo_remove_outlier_1.5factor_"


    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_perf_change_dir + "perf_two_result_add_num_set_compreh.csv", index=False)

    # dataMain.to_csv(csv_perf_change_dir + "perf_two_result.csv", index=False)


import sys, ast, os, csv, time, copy
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import util
import performance_util
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':

    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_1st_invo_step_100/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_1.5factor/"


    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_2_50_invocations/"

    save_code_info_dir_add_performance_change = \
        util.data_root +"performance/tosem_2020_list_compre_bench_rq_1_2nd_invo_step_100/50/"



    # dict_pd=performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change)
    dict_pd=performance_util.get_ci_perf_change_dict_add_num_ele_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    print(
        f"total number of {len(os.listdir(save_code_info_dir_add_performance_change))} files in perf_dir, {len(set(dict_pd['file_html']))}file_html,"
        f" {len(dict_pd['test_me_inf'])}, {len(set(dict_pd['test_me_inf']))} test method,"
        f" {len(dict_pd['instance'])}, {len(set(dict_pd['instance']))}test instances: ")

    perf_improve_list=dict_pd['perf_change']
    RCIW_zonghe_list =  dict_pd["RCIW"]
    print("count,mean, median, min, max: ",len(perf_improve_list), np.mean(perf_improve_list), np.median(perf_improve_list), np.min(perf_improve_list), np.max(perf_improve_list))
    print("rciw count,mean, median, min, max: ", len(RCIW_zonghe_list), np.mean(RCIW_zonghe_list),
          np.median(RCIW_zonghe_list), np.min(RCIW_zonghe_list),
          np.max(RCIW_zonghe_list))
    plt.boxplot(perf_improve_list)
    plt.show()
    perf_regression_list=dict_pd['perf_change_rm_outlier']
    RCIW_zonghe_list =  dict_pd["RCIW_rm_outlier"]
    print("count,mean, median, min, max: ", len(perf_regression_list), np.mean(perf_regression_list),np.median(perf_regression_list), np.min(perf_regression_list), np.max(perf_regression_list))
    print("rciw count,mean, median, min, max: ", len(RCIW_zonghe_list), np.mean(RCIW_zonghe_list),
          np.median(RCIW_zonghe_list), np.min(RCIW_zonghe_list),
          np.max(RCIW_zonghe_list))
    plt.boxplot(perf_regression_list)
    plt.show()

    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv/"
    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_remove_outlier/"
    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_remove_outlier_1.5factor/"
    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_remove_outlier_2_50_invocations/"
    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_remove_outlier_2_50_invocations_3factor/"
    csv_perf_change_dir = util.data_root + "performance/a_list_comprehension/"
    # os.mkdir(csv_perf_change_dir)
    # csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_2_50_invocations/"
    prefix_csv_perf_change="remove_outlier_"
    prefix_csv_perf_change = "remove_outlier_1.5factor_"
    prefix_csv_perf_change = "2nd_invo_remove_outlier_3_factor_"
    prefix_csv_perf_change = "2nd_invo_remove_outlier_1.5factor_"

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
    # dataMain = pd.DataFrame(data=perf_improve_dict)
    # dataMain.to_csv(csv_perf_change_dir + "perf_two_result.csv", index=False)
    # csv_perf_change_dir = util.data_root_mv + "performance/a_truth_value_test/csv/"
    # if not os.path.exists(csv_perf_change_dir):
    #     os.mkdir(csv_perf_change_dir)
    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_perf_change_dir + "list_comprehension_perf_two_result.csv", index=False)

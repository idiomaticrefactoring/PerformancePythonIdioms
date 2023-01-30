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
    large_1_dir = util.data_root_mv + "performance/a_multi_assign/large_1/"

    file_html_list_filter = util.load_pkl(large_1_dir, "large_1_info")
    print("len: ",len(file_html_list_filter))
    #'''
    
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_multi_assign/a_multi_assign_iter_invoca_add_perf_change_new/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_multi_assign/a_multi_assign_iter_invoca_add_perf_change_new_merge/"

    # save_code_info_dir_add_performance_change=util.data_root_mv + "performance/chain_compare/chain_compare_iter_invoca_new/50/"
    # save_code_info_dir_add_performance_change=util.data_root + "performance/chain_compare/chain_compare_iter_invoca/"


    # save_code_info_dir_add_performance_change_remove_outlier = \
    #     util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_2_50_invocations/"
    #
    # save_code_info_dir_add_performance_change = \
    #     util.data_root +"performance/tosem_2020_list_compre_bench_rq_1_2nd_invo_step_100/50/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_multi_assign/a_multi_assign_iter_invoca_add_perf_change_new_remove_outlier/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_multi_assign/a_multi_assign_iter_invoca_add_perf_change_new_remove_outlier_merge/"



    # dict_pd=performance_util.get_ci_perf_change_dict_merge(save_code_info_dir_add_performance_change)
    dict_pd=performance_util.get_ci_perf_change_dict_merge_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
    # perf_improve_list=perf_improve_dict['perf_change']
    print(
        f"total number of {len(os.listdir(save_code_info_dir_add_performance_change))} files in perf_dir, {len(set(dict_pd['file_html']))}file_html,"
        f" {len(dict_pd['test_me_inf'])}, {len(set(dict_pd['test_me_inf']))} test method,"
        f" {len(dict_pd['instance'])}, {len(set(dict_pd['instance']))}test instances: ")

    perf_improve_list=dict_pd['perf_change']
    perf_improve_list_original = dict_pd['perf_change']
    RCIW_list = dict_pd['RCIW']
    large_1_list = [i for i, e in enumerate(perf_improve_list) if e > 1]


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
    plt.boxplot(perf_improve_list)
    plt.show()
    large_1_rm_outlier_list = [i for i, e in enumerate(perf_improve_list) if e > 1]

    perf_change_zonghe_list=[]
    RCIW_zonghe_list=[]
    for i,e in enumerate(dict_pd['RCIW_rm_outlier']):
        if dict_pd['RCIW'][i]>e:
            perf_change_zonghe_list.append(perf_improve_list[i])
            RCIW_zonghe_list.append(e)
        else:
            perf_change_zonghe_list.append(perf_improve_list_original[i])
            RCIW_zonghe_list.append(dict_pd['RCIW'][i])
    large_1_zonghe=[i for i, e in enumerate(perf_change_zonghe_list) if e > 1]
    plt.boxplot(perf_change_zonghe_list)
    plt.show()
    print("num of large than 1 original, rm_outlier and zonghe: ",
          len(large_1_list),len(large_1_rm_outlier_list),len(large_1_zonghe))
    dict_pd["perf_change_zonghe"] = perf_change_zonghe_list
    dict_pd["RCIW_zonghe"] = RCIW_zonghe_list
    print("count,mean, median, min, max: ", len(perf_change_zonghe_list), np.mean(perf_change_zonghe_list),
          np.median(perf_change_zonghe_list), np.min(perf_change_zonghe_list), np.max(perf_change_zonghe_list))
    print("count,mean, median, min, max: ", len(RCIW_zonghe_list), np.mean(RCIW_zonghe_list), np.median(RCIW_zonghe_list), np.min(RCIW_zonghe_list),
          np.max(RCIW_zonghe_list))
    # large_1=[i for i,e in enumerate(perf_improve_list) if e>1]
    # file_html_list=dict_pd['file_html']
    # file_html_list_filter=[file_html_list[i] for i,e in enumerate(file_html_list) if i in large_1]
    # large_1_dir=util.data_root_mv + "performance/a_multi_assign/large_1/"
    # util.save_pkl(large_1_dir, "large_1_info", file_html_list_filter)
    # print("len: ",len(file_html_list_filter))
    # print("len: ", file_html_list_filter)




    # print("count,mean, median, min, max: ", len(perf_regression_list), np.mean(perf_regression_list),np.median(perf_regression_list), np.min(perf_regression_list), np.max(perf_regression_list))


    csv_perf_change_dir = util.data_root + "performance/a_multi_assign/csv/"
    # os.mkdir(csv_perf_change_dir)
    # csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_2_50_invocations/"
    prefix_csv_perf_change="remove_outlier_3factor_"
    # prefix_csv_perf_change = "remove_outlier_1.5factor_"
    # prefix_csv_perf_change = "2nd_invo_remove_outlier_3_factor_"
    # prefix_csv_perf_change = "2nd_invo_remove_outlier_1.5factor_"


    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_perf_change_dir + "perf_two_result_merge_multi_ass.csv", index=False)

    # dataMain.to_csv(csv_perf_change_dir + prefix_csv_perf_change+"perf_two_result_merge.csv", index=False)
    # dataMain.to_csv(csv_perf_change_dir + prefix_csv_perf_change+"perf_two_result.csv", index=False)

    # dataMain.to_csv(csv_perf_change_dir + "perf_two_result.csv", index=False)
#'''

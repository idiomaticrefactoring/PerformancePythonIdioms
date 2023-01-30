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


    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/a_list_comprehension/perf_change_remove_outlier_2_50_invocations/"
    '''
    save_code_info_dir_add_performance_change = \
        util.data_root +"performance/tosem_2020_list_compre_bench_rq_1_2nd_invo_step_100/50/"
    '''
    perf_improve_dict=dict()#{
    #     "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    # }
    perf_regression_dict=dict()#{
    #     "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    # }
    perf_unchange_dict =dict()# {
    #     "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    # }

    # dict_pd=performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change)
    dict_pd=performance_util.get_ci_perf_change_dict_add_num_ele(save_code_info_dir_add_performance_change)

    for key in dict_pd:
        perf_improve_dict[key]=[]
        perf_regression_dict[key]=[]
        perf_unchange_dict[key]=[]
    perf_change_left=dict_pd['perf_change_left']
    perf_change_right=dict_pd['perf_change_right']
    for ind,e in enumerate(perf_change_right):
        low=perf_change_left[ind]
        if low<=1<=e:
            for key in dict_pd:
                perf_unchange_dict[key].append(dict_pd[key][ind])
        elif low>1:
            for key in dict_pd:
                perf_improve_dict[key].append(dict_pd[key][ind])
        else:
            for key in dict_pd:
                perf_regression_dict[key].append(dict_pd[key][ind])

    print("total count: ",len(perf_change_right))
    perf_unchange_list=perf_unchange_dict['perf_change']
    plt.boxplot(perf_unchange_list)
    print("count,mean, median, min, max: ",len(perf_unchange_list), np.mean(perf_unchange_list),np.median(perf_unchange_list), np.min(perf_unchange_list), np.max(perf_unchange_list))
    plt.show()
    perf_improve_list=perf_improve_dict['perf_change']
    print("count,mean, median, min, max: ",len(perf_improve_list), np.mean(perf_improve_list), np.median(perf_improve_list), np.min(perf_improve_list), np.max(perf_improve_list))
    plt.boxplot(perf_improve_list)
    plt.show()
    perf_regression_list=perf_regression_dict['perf_change']
    print("count,mean, median, min, max: ", len(perf_regression_list), np.mean(perf_regression_list),np.median(perf_regression_list), np.min(perf_regression_list), np.max(perf_regression_list))
    plt.boxplot(perf_regression_list)
    plt.show()

    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv/"
    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_remove_outlier/"
    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_remove_outlier_1.5factor/"
    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_remove_outlier_2_50_invocations/"
    csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_remove_outlier_2_50_invocations_3factor/"

    # os.mkdir(csv_perf_change_dir)
    # csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_2_50_invocations/"
    prefix_csv_perf_change="remove_outlier_"
    prefix_csv_perf_change = "remove_outlier_1.5factor_"
    prefix_csv_perf_change = "2nd_invo_remove_outlier_3_factor_"
    prefix_csv_perf_change = "2nd_invo_remove_outlier_1.5factor_"

    dataMain = pd.DataFrame(data=perf_unchange_dict)
    dataMain.to_csv(csv_perf_change_dir + prefix_csv_perf_change+"perf_unchange_dict.csv", index=False)

    dataMain = pd.DataFrame(data=perf_improve_dict)
    dataMain.to_csv(csv_perf_change_dir + prefix_csv_perf_change+"perf_improve_dict.csv", index=False)

    dataMain = pd.DataFrame(data=perf_regression_dict)
    dataMain.to_csv(csv_perf_change_dir + prefix_csv_perf_change+"perf_regression_dict.csv", index=False)


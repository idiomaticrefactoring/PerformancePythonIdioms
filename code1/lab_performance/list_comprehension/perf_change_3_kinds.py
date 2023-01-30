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
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new_add_perf_change/50/"
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

    csv_perf_change_dir=util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/csv/"

    dataMain = pd.DataFrame(data=perf_unchange_dict)
    dataMain.to_csv(csv_perf_change_dir + "perf_unchange_dict.csv", index=False)

    dataMain = pd.DataFrame(data=perf_improve_dict)
    dataMain.to_csv(csv_perf_change_dir + "perf_improve_dict.csv", index=False)

    dataMain = pd.DataFrame(data=perf_regression_dict)
    dataMain.to_csv(csv_perf_change_dir + "perf_regression_dict.csv", index=False)


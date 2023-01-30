import sys, ast, os, csv, time, copy,shutil
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
import util
import lab_performance_util
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def cp_file(base_dir,source_dir,des_dir):
    source_file_name_list=[e[:-4] for e in os.listdir(source_dir)]
    count=0
    for e in os.listdir(base_dir):
        file_name=e[:-3]
        pkl_file_name=file_name+".pkl"
        # print(pkl_file_name)
        if pkl_file_name not in os.listdir(des_dir):
            shutil.copyfile(source_dir+pkl_file_name,des_dir+pkl_file_name)
            count+=1
            pass
        # else:
        #     print(pkl_file_name," existed")
        # count += 1
    print("count: ",count)


if __name__ == '__main__':
    bench_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/code/code/"
    total_file_list=[e[:-3] for e in os.listdir(bench_dir)]
    print(len(total_file_list))
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new_add_perf_change_remove_outlier/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/prefined_cpus_remain_code_new_add_perf_change/50/"
    save_code_info_dir_add_performance_change_remove_outlier = \
        util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/prefined_cpus_remain_code_new_add_perf_change_remove_outlier/50/"

    # save_code_info_dir_add_performance_change_1 = \
    #     util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/prefined_cpus_remain_code_new_add_perf_change/50/"
    # save_code_info_dir_add_performance_change_remove_outlier_1 = \
    #     util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/prefined_cpus_remain_code_new_add_perf_change_remove_outlier/50/"
    # print("len: ",len(os.listdir(save_code_info_dir_add_performance_change_remove_outlier_1)),
    #       len(os.listdir(save_code_info_dir_add_performance_change_1)))
    # print("len: ", len(os.listdir(save_code_info_dir_add_performance_change_remove_outlier)),
    #       len(os.listdir(save_code_info_dir_add_performance_change)))
    # cp_file(bench_dir, save_code_info_dir_add_performance_change, save_code_info_dir_add_performance_change_1)
    # cp_file(bench_dir, save_code_info_dir_add_performance_change_remove_outlier, save_code_info_dir_add_performance_change_remove_outlier_1)

    # exist_file_list = list(os.listdir(save_code_info_dir_add_performance_change_remove_outlier_1))
    file_name_list=list(os.listdir(save_code_info_dir_add_performance_change_remove_outlier))
    '''
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
    #         break
    # for file_name in os.listdir(save_code_info_dir_add_performance_change):
    #     print(file_name)
    #     break
    '''
    perf_improve_dict={
        "file_html": [], "code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    }
    perf_regression_dict={
        "file_html": [], "code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    }
    perf_unchange_dict = {
        "file_html": [], "code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []
    }
    dict_pd=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change,1,file_name_list)
    dict_pd_remove_outlier=lab_performance_util.get_ci_perf_change_dict(save_code_info_dir_add_performance_change_remove_outlier,1,file_name_list)
    for key in dict_pd_remove_outlier:
        if key not in ["file_html","code_str"]:
            dict_pd[key+"_rm_outlier"]=[]
    for file_html in dict_pd["file_html"]:
        index=dict_pd_remove_outlier["file_html"].index(file_html)
        for key in dict_pd_remove_outlier:
            if key not in ["file_html","code_str"]:
                dict_pd[key+"_rm_outlier"].append(dict_pd_remove_outlier[key][index])

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
    csv_perf_change_dir = util.data_root + "lab_performance/list_compre_benchmarks_fun_and_Nfunc/csv/"

    dataMain.to_csv(csv_perf_change_dir + "two_configure_perf_change_ci_list_comprehension.csv", index=False)
    # '''



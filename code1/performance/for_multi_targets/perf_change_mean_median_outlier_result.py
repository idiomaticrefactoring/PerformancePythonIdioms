import sys, ast, os, csv, time, copy
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
from extract_transform_complicate_code_new.extract_compli_var_unpack_for_target_improve_new import get_for_target_add_info,get_for_target

import util
import performance_util
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def get_ci_perf_change_dict_merge_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {
        "file_html": [], "test_me_inf":[], "instance":[],"code_str": [],
        'perf_change': [], 'perf_change_left': [], 'perf_change_right': [], 'RCIW': [],
        'perf_change_rm_outlier': [], 'perf_change_left_rm_outlier': [], 'perf_change_right_rm_outlier': [], 'RCIW_rm_outlier': []
        ,"num_unpack":[],"num_subscript":[]
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
        old_tree, new_tree = lab_code_info.code_info
        new_code_list = get_for_target_add_info(old_tree)

        # continue
        file_html = lab_code_info.file_html
        code_str = lab_code_info.get_code_str()
        # print(lab_code_info.__dict__)
        perf_info_dict = lab_code_info.perf_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:

        for ind_tm,test_me in enumerate(perf_info_dict):

            for instance in perf_info_dict[test_me]:
                # print(test_me)

                for old_tree, new_tree, var_list_real, Map_Var in new_code_list:
                    var_list_real_str=[ast.unparse(e) for e in var_list_real]
                    # print("old_tree: ", ast.unparse(old_tree))
                    # print("new_tree: ", ast.unparse(new_tree))
                    # print("Map_Var: ", Map_Var)
                    # print("var_list_real: ", var_list_real)
                    dict_pd["num_unpack"].append(len(set(var_list_real_str)))
                    dict_pd["num_subscript"].append(len(var_list_real_str))
                perf_info = perf_info_dict[test_me][instance]
                # if file_html == "https://github.com/indigo-dc/udocker/tree/master/udocker/docker.py" and perf_info[0]<0.5:
                #     continue
                test_me_list.add(file_name_no_suffix + str(test_me))
                file_name_list.add(file_name_no_suffix)
                print("perf_info: ", file_name, test_me,perf_info)
                perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
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
        # break
    print("len of file and test methods: ",len(file_name_list),len(test_me_list))
    return dict_pd
if __name__ == '__main__':
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_total_data/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_set_comprehension/a_set_comprehension_iter_invoca_add_perf_change_new_merge/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_call_star/a_call_star_iter_invoca_add_perf_change_new_merge/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_multi_tar/a_for_multi_tar_iter_invoca_add_perf_change_new_merge/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_multi_tar_single/a_for_multi_tar_iter_invoca_add_perf_change_new_merge_2/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_multi_tar_single/a_for_multi_tar_iter_invoca_add_perf_change_new_merge_2/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_multi_tar_single_2/a_for_multi_tar_iter_invoca_add_perf_change_new_merge_2/"


    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_remove_outlier_total_data/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_set_comprehension/a_set_comprehension_iter_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_set_comprehension/a_set_comprehension_iter_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_call_star/a_call_star_iter_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_for_multi_tar/a_for_multi_tar_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_for_multi_tar_single/a_for_multi_tar_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change_remove_outlier=util.data_root_mv + "performance/a_for_multi_tar_single_2/a_for_multi_tar_iter_invoca_add_perf_change_new_merge_2_remove_outlier/"


    # dict_pd=performance_util.get_ci_perf_change_dict_merge(save_code_info_dir_add_performance_change)
    dict_pd=get_ci_perf_change_dict_merge_two_dirs(save_code_info_dir_add_performance_change,save_code_info_dir_add_performance_change_remove_outlier)
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
    csv_perf_change_dir=util.data_root_mv + "performance/a_for_multi_tar_single_2/csv/"
    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    # csv_perf_change_dir=util.data_root + "performance/a_list_comprehension/csv_2_50_invocations/"
    prefix_csv_perf_change="remove_outlier_3factor_"
    # prefix_csv_perf_change = "remove_outlier_1.5factor_"
    # prefix_csv_perf_change = "2nd_invo_remove_outlier_3_factor_"
    # prefix_csv_perf_change = "2nd_invo_remove_outlier_1.5factor_"


    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_perf_change_dir + "a_for_multi_tar_single_perf_two_result_total.csv", index=False)

    # dataMain.to_csv(csv_perf_change_dir + "perf_two_result.csv", index=False)


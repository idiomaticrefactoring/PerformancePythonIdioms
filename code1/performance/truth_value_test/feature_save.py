import sys,ast,os,csv,time,copy,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")

import util, performance_util
from code_info import CodeInfo
import pandas as pd

def save_features_add_interval(save_code_info_dir_add_performance_change_remove_outlier):
    dict_pd = {"file_html":[],"test_me_inf":[],"instance":[],
               "code_str":[],"node_kind":[],"data_type":[],
               "perf_change":[],"perf_change_left_rm_outlier":[],
               "perf_change_right_rm_outlier":[],"RCIW":[]}
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change_remove_outlier)):
        print("file_name: ",file_name)
        file_name_no_suffix = file_name[:-4]

        try:
            lab_code_info_remove_outlier = util.load_pkl(save_code_info_dir_add_performance_change_remove_outlier,
                                                     file_name_no_suffix)
            lab_code_info_remove_outlier_data_type = util.load_pkl(data_type_code_info_dir,
                                                         file_name_no_suffix)
        except:
            print(">>>> the file cannot load: ",save_code_info_dir_add_performance_change_remove_outlier,file_name_no_suffix)
            continue
        perf_info_dict_remove_outlier = lab_code_info_remove_outlier.perf_info_dict
        type_add_list=lab_code_info_remove_outlier_data_type.type_add_list
        lab_code_info_remove_outlier: CodeInfo
        file_html = lab_code_info_remove_outlier.file_html
        code_str = lab_code_info_remove_outlier.get_code_str()
        # # print(lab_code_info.__dict__)
        # perf_info_dict = lab_code_info.perf_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        old_tree, new_tree = lab_code_info_remove_outlier.code_info
        print("code: ",ast.unparse(old_tree),ast.unparse(old_tree.left),old_tree,old_tree.left)
        # print(perf_info_dict_remove_outlier)
        # print(type_add_list)#type_add_list[test_me][instance])
        # break
        for ind_tm,test_me in enumerate(perf_info_dict_remove_outlier):

            for instance in perf_info_dict_remove_outlier[test_me]:
                # print(type_add_list[test_me][instance][0][0][1])
                node_str=performance_util.get_node_kind(old_tree.left)
                # if node_str=="Other":
                #     continue
                dict_pd["node_kind"].append(node_str)
                dict_pd["data_type"].append(type_add_list[test_me][instance][0][0][1])
                # print(test_me)

                # perf_info = perf_info_dict[test_me][instance]
                # print("perf_info: ", file_name, test_me,perf_info)
                perf_info_remove_outlier = perf_info_dict_remove_outlier[test_me][instance]
                # print("perf_info: ", file_name, test_me, perf_info, perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))
                # # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)
                #
                # dict_pd["perf_change"].append(perf_info[0])
                # dict_pd["perf_change_left"].append(perf_info[1])
                # dict_pd["perf_change_right"].append(perf_info[2])
                dict_pd["perf_change"].append(perf_info_remove_outlier[0])

                # dict_pd["perf_change_rm_outlier"].append(perf_info_remove_outlier[0])
                dict_pd["perf_change_left_rm_outlier"].append(perf_info_remove_outlier[1])
                dict_pd["perf_change_right_rm_outlier"].append(perf_info_remove_outlier[2])
                dict_pd["RCIW"].append((perf_info_remove_outlier[2] - perf_info_remove_outlier[1]) / perf_info_remove_outlier[0])
                # dict_pd["RCIW_rm_outlier"].append(
                #     (perf_info_remove_outlier[2] - perf_info_remove_outlier[1]) / perf_info_remove_outlier[0])

        # break
    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)


if __name__ == '__main__':
    bench_time_info_dir=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_total_data/"
    bench_time_info_dir=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge_total_data/"
    data_type_code_info_dir = util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_total_data_add_type/"

    csv_feature_file_name_corr= util.data_root_mv + "performance/a_truth_value_test/csv/performance_truth_value_test_feature.csv"
    csv_feature_file_name_corr= util.data_root_mv + "performance/a_truth_value_test/csv/performance_truth_value_test_feature_total_data.csv"

    save_features_add_interval(bench_time_info_dir)
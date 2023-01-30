import sys, ast, os, csv, time, copy

import subprocess
from pathos.multiprocessing import ProcessingPool as newPool

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import pandas as pd
import util, performance_util
from code_info import CodeInfo
from scipy.stats import ranksums, mannwhitneyu
import cliffsDelta
def save_perf_change(file_name,merge,bench_time_info_dir,save_code_info_dir_add_performance_change):

    file_name_no_suffix = file_name[:-4]
    lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
    lab_code_info: CodeInfo

    # print("total_time_list_info_dict: ",total_time_list_info_dict)
    # for invo in invo_list:


    lab_code_info.get_performance_improve_info(total_time_list_info_dict=dict(), invocations=50, steps=100,merge=merge, remove_outlier=True, factor=3)
    # print("performance change: ",lab_code_info.total_time_list_info_dict)
    util.save_pkl(save_code_info_dir_add_performance_change  + "/", file_name_no_suffix, lab_code_info)
    print("save ",save_code_info_dir_add_performance_change  + "/", file_name_no_suffix, "successfully")
    pass

def save_csv_perf_change(save_code_info_dir_add_performance_change,csv_perf_change_dir):
    dict_pd={
        "file_html":[],"test_me_inf":[], "code_str":[],'perf_change':[],'RCIW':[],'perf_change_left':[],'perf_change_right':[]

    }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix=file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        lab_code_info: CodeInfo
        file_html=lab_code_info.file_html
        code_str=lab_code_info.get_code_str()
        perf_info_dict=lab_code_info.perf_info_dict
        print("file_name: ",file_name,perf_info_dict)
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                perf_info=perf_info_dict[test_me][instance]
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["RCIW"].append(perf_info[3])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])

    dataMain = pd.DataFrame(data=dict_pd)
    # print(">>>>>>drop same features: ", dataMain.keys())
        # print(dataMain.to_dict())
    dataMain.to_csv(csv_perf_change_dir+"csv_perf_change_result.csv", index=False)

if __name__ == '__main__':
    start_time=time.time()
    # save_code_info_dir =util.data_root + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change/"
    # save_code_info_dir=util.data_root_mv+"performance/a_truth_value_test/a_truth_value_test_iter_invoca/"

    # save_code_info_dir=util.data_root_mv+"performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_some/"


    bench_time_info_dir=util.data_root+"performance/a_truth_value_test/a_truth_value_test_iter_invoca/"
    bench_time_info_dir=util.data_root_mv+"performance/a_set_comprehension/set_comprehension_iter_invoca/"
    bench_time_info_dir=util.data_root_mv+"performance/a_call_star/a_call_star_iter_invoca/"
    bench_time_info_dir=util.data_root_mv+"performance/a_for_multi_tar/a_for_multi_tar_iter_invoca/"
    bench_time_info_dir = util.data_root_mv + "performance/a_for_else/a_for_else_tar_iter_invoca/"
    bench_time_info_dir = util.data_root_mv + "performance/a_for_else/a_for_else_tar_iter_invoca_2/"

    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new/"

    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_truth_value_test/a_truth_value_test_iter_invoca_add_perf_change_new_merge/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_set_comprehension/a_set_comprehension_iter_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_call_star/a_call_star_iter_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_multi_tar/a_for_multi_tar_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_else/a_for_else_iter_invoca_add_perf_change_new_merge_remove_outlier/"
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_for_else/a_for_else_iter_invoca_add_perf_change_new_merge_remove_outlier_2/"

    csv_perf_change_dir=util.data_root + "performance/a_for_else/csv/"
    file_name_list=[]
    for ind, file_name in enumerate(sorted(os.listdir(bench_time_info_dir)[:])):
        # break
        if  file_name.endswith('.log'):
            print(file_name)
            continue

        fsize = os.path.getsize(bench_time_info_dir+file_name)
        fsize = fsize / float(1024 * 1024)
        if fsize>1000:
            print(f"{fsize}MB too large file_name: ", bench_time_info_dir, file_name)
            continue
        file_name_list.append(file_name)
        # break
        # print("fsize: ",fsize)
        # break
    #     if ind>2:
    #         break
    # pass
    print("total file name: ",len(file_name_list))
    #'''

    merge_list, bench_time_info_dir_list, save_code_info_dir_add_performance_change_list=\
        [1 for i in range(len(file_name_list))],[bench_time_info_dir for i in range(len(file_name_list))],[save_code_info_dir_add_performance_change for i in range(len(file_name_list))]
    pool = newPool(nodes=30)
    # pool.map(save_perf_change, file_name_list[:1],merge_list[:1],bench_time_info_dir_list[:1],save_code_info_dir_add_performance_change_list[:1])  # [:3]sample_repo_url ,token_num_list[:1]
    pool.map(save_perf_change, file_name_list[:],merge_list[:],bench_time_info_dir_list[:],save_code_info_dir_add_performance_change_list[:])  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    #'''

    # save_csv_perf_change(save_code_info_dir_add_performance_change+str(invo)+"/", csv_perf_change_dir)
    print("total project time: ",time.time()-start_time)

import sys, ast, os, csv, time, copy

import subprocess
from pathos.multiprocessing import ProcessingPool as newPool

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
import pandas as pd
import util,lab_performance_util
from lab_code_info import LabCodeInfo
def save_perf_change(file_name,bench_time_info_dir,save_code_info_dir_add_performance_change,invo=50):

    file_name_no_suffix = file_name[:-4]
    lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
    lab_code_info: LabCodeInfo

    # print("total_time_list_info_dict: ",total_time_list_info_dict)
    # for invo in invo_list:
    lab_code_info.get_performance_improve_info(remove_outlier=True,factor=3)
    print("performance change: ",lab_code_info.perf_ci_info)
    util.save_pkl(save_code_info_dir_add_performance_change + str(invo) + "/", file_name_no_suffix, lab_code_info)
    print("save ",save_code_info_dir_add_performance_change + str(invo) + "/", file_name_no_suffix, "successfully")
    pass

def save_csv_perf_change(save_code_info_dir_add_performance_change,csv_perf_change_dir,csv_file_name="csv_perf_change_result.csv"):
    dict_pd={
        "file_html":[],"code_str":[],'perf_change':[],'RCIW':[],'perf_change_left':[],'perf_change_right':[]

    }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix=file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        file_html=lab_code_info.file_path
        code_str=lab_code_info.get_code_str()
        perf_info_dict=lab_code_info.perf_ci_info
        print("file_name: ",file_name,perf_info_dict)
        if 1:
        # for test_me in perf_info_dict:
        #     for instance in perf_info_dict[test_me]:
                perf_info=perf_info_dict
                dict_pd["file_html"].append(file_html)
                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["RCIW"].append(perf_info[3])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])

    dataMain = pd.DataFrame(data=dict_pd)
    # print(">>>>>>drop same features: ", dataMain.keys())
        # print(dataMain.to_dict())
    dataMain.to_csv(csv_perf_change_dir+csv_file_name, index=False)
if __name__ == '__main__':
    start_time=time.time()
    bench_time_info_dir=util.data_root + "lab_performance/multi_ass_benchmarks/bench_time_info_dir_prefined_cpu_new/"

    save_code_info_dir_add_performance_change=\
        util.data_root + "lab_performance/multi_ass_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    # save_code_info_dir =util.data_root + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change/"
    # bench_time_info_dir=util.data_root + "performance/chain_compare/chain_compare_iter_invoca/"
    # save_code_info_dir_add_performance_change=util.data_root_mv + "performance/chain_compare/chain_compare_iter_invoca_add_perf_change/"
    csv_perf_change_dir=util.data_root + "lab_performance/multi_ass_benchmarks/csv/"
    if not os.path.exists(csv_perf_change_dir):
        os.mkdir(csv_perf_change_dir)
    file_name_list=[]
    invo = 50
    count=0
    for ind, file_name in enumerate(sorted(os.listdir(bench_time_info_dir)[:])):
        # print("file_name: ",file_name)
        # break
        if file_name!="5_ass_const_func.pkl":#"6_ass_swap_func.py":
            continue
        file_name_list.append(file_name)
        count+=1
        # if ind>2:
        #     break
    print("count of files: ",count)

    # pass
    #'''
    bench_time_info_dir_list, save_code_info_dir_add_performance_change_list=\
        [bench_time_info_dir for i in range(len(file_name_list))],\
        [save_code_info_dir_add_performance_change for i in range(len(file_name_list))]
    pool = newPool(nodes=15)
    pool.map(save_perf_change, file_name_list[:],bench_time_info_dir_list,save_code_info_dir_add_performance_change_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    #'''
    #'''list_comprehension
    # os.mkdir(csv_perf_change_dir)
    save_csv_perf_change(save_code_info_dir_add_performance_change+str(invo)+"/", csv_perf_change_dir,csv_file_name="csv_perf_change_result_remove_outlier.csv")
    print("total project time: ",time.time()-start_time)
    #'''

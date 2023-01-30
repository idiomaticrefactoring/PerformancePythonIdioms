import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_list_comprehension
import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util
from lab_code_info import LabCodeInfo


if __name__ == '__main__':
    #code_time_info_no_isolated code_time_info_prefined_cpu
    bench_time_info_dir_list=["code_time_info_prefined_cpu",
                              "code_time_info_prefiend_cpu_multip_1",
                              "code_time_info_prefiend_cpu_multip_2",
                              "code_time_info_no_isolated","code_time_info_complete","code_time_info"]

    for dir_e in bench_time_info_dir_list[:]:
        bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/different_sys_set/"+dir_e+"/"
        print(dir_e)
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
            # if ind>10:
            #     break
            # if file_name!="2_4_3_[1].pkl":#"1_1_0_list(range(1,11))*10.pkl":#
            #     continue
            print("file_name: ",file_name)
            file_name_no_suffix = file_name[:-4]
            lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
            lab_code_info: LabCodeInfo
            # print("code path: ",lab_code_info.file_path)
            invocations, iterations, num_add_ele = lab_code_info.invocations, lab_code_info.iterations, lab_code_info.num_add_ele
            num_for, num_if, num_if_else, e_input = file_name_no_suffix.split("_")

            time_list = lab_code_info.compli_code_time_dict
            idiom_time_list = lab_code_info.simple_code_time_dict



            # print(">>>>time_list: ", time_list)
            # print(">>>>idiom_time_list: ",idiom_time_list)
            warms_up=3
            window=4
            time_list = [[float(e) for e in e_list[warms_up:]] for e_list in time_list]
            idiom_time_list = [[float(e) for e in e_list[warms_up:]] for e_list in idiom_time_list]
            for ind_t,e in enumerate(time_list):
                print(">>>>>ind_t: ",ind_t)
                for i in range(len(e)-window+1):
                    cov=np.std(e[i:i+window]) / np.mean(e[i:i+window])
                    print(f"{i} cov: ",cov)
            print("time_list: ",np.mean(time_list),np.std(time_list),np.std(time_list)/np.mean(time_list))
            print("idiom_time_list: ",np.mean(idiom_time_list),np.std(idiom_time_list),np.std(idiom_time_list)/np.mean(idiom_time_list))

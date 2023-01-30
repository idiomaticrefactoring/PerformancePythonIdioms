import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_list_comprehension
import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util
from lab_code_info import LabCodeInfo


if __name__ == '__main__':
    #code_time_info_no_isolated code_time_info_prefined_cpu
    bench_time_info_dir_list=["code_time_info_prefined_cpu","remain_code/prefined_cpus_remain_code",
                              "remain_code_1/prefined_cpus_remain_code/", "code_base/code_time_info"]#code_base
    bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/code/code_base/"#code/

    remain_dir=util.data_root + "lab_performance/list_compre_benchmarks/prefined_cpus_remain_code_2/"
    bench_final_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks/final_stable/"

    # util.mkdirs(remain_dir)
    file_name_stable_list=[]
    file_name_list=set([])
    for dir_e in bench_time_info_dir_list[1:2]:
        bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/"+dir_e+"/"
        # print(dir_e)
        print(f"total file of benchmarks in {bench_time_info_dir} is: ", len(os.listdir(bench_time_info_dir)))
        total_unstable_count = 0
        total_unstable_invo_count=0
        # file_name_list=[]
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
            file_name_list.add(file_name)
            if file_name in file_name_stable_list:
                continue
            # if ind>10:
            #     break
            # if file_name!="2_4_3_[1].pkl":#"1_1_0_list(range(1,11))*10.pkl":#
            #     continue
            # print("file_name: ",file_name)
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
            # print("len of time list: ",len(time_list),len(idiom_time_list))
            # file_unstable_count=lab_performance_util.whether_time_list_within_cov(idiom_time_list,window)
            # file_unstable_count+=lab_performance_util.whether_time_list_within_cov(time_list,window)
            '''
            file_unstable_count = lab_performance_util.whether_time_list_within_cov_for_given_number(idiom_time_list, window)
            file_unstable_count += lab_performance_util.whether_time_list_within_cov_for_given_number(time_list, window)
            if file_unstable_count:

                # print(f"{file_name} don't reach stable with {file_unstable_count} invocations")
                total_unstable_count+=1
                total_unstable_invo_count+=file_unstable_count
                file_name_list.append(file_name[:-4]+".py")
            else:
                file_name_stable_list.append(file_name)
            '''
            valid_time_list,index_list=lab_performance_util.get_time_list_within_cov_contain_index(time_list, window)
            if len(valid_time_list)<10:
                continue
            valid_idiom_time_list,index_idiom_list=lab_performance_util.get_time_list_within_cov_contain_index(idiom_time_list, window)
            if len(valid_idiom_time_list)<10:
                continue
            for e in index_list:
                if e > 6:
                    print("iterations of complicated code  are larger than 10: ",e)
            for e in index_idiom_list:
                if e > 6:
                    print("iterations of simple code are larger than 10: ",e)
            file_name_stable_list.append(file_name)
            # util.save_pkl(bench_final_time_info_dir, file_name[:-3], lab_code_info)

            #
            # for ind_t, e in enumerate(time_list):
            #     # print(">>>>>ind_t: ",ind_t)
            #     for i in range(len(e) - window + 1):
            #         cov = np.std(e[i:i + window]) / np.mean(e[i:i + window])
            #         if cov <= 0.02:
            #             valid_count_invoca += 1
            #             break
            #     else:
            #         file_unstable_count += 1
                    # print(f"{file_name} don't reach stable in {ind_t+1} invocations")
            # if valid_count_invoca<10:
            #     print(f"{file_name} don't reach stable within 30 invocations")


        print("total_unstable_count,total_unstable_invo_count: ",total_unstable_count)
        # print("total count of unstable files: ",len(file_name_list),len(set(file_name_list)))
        '''
        util.save_json(remain_dir,"prefined_cpus_remain_unstable",file_name_list)
        file_name_list=util.load_json(remain_dir,"prefined_cpus_remain_unstable")
        print("file_name_list: ",len(file_name_list),file_name_list[0])
        '''
            # print("time_list: ",np.mean(time_list),np.std(time_list),np.std(time_list)/np.mean(time_list))
            # print("idiom_time_list: ",np.mean(idiom_time_list),np.std(idiom_time_list),np.std(idiom_time_list)/np.mean(idiom_time_list))
    print("total stable file name list: ",len(file_name_stable_list),len(set(file_name_stable_list)),len(file_name_list))
    print("remain list: ",len(file_name_list-set(file_name_stable_list)),file_name_list-set(file_name_stable_list))
    '''
    a=[e[:-4]+".py" for e in list(file_name_list - set(file_name_stable_list))]
    util.save_json(remain_dir, "prefined_cpus_remain_unstable", a)
    file_name_list = util.load_json(remain_dir, "prefined_cpus_remain_unstable")
    print("len remain of files: ",len(file_name_list))
    print(file_name_list)
    '''
    print("final state performance: ", len(os.listdir(bench_final_time_info_dir)))

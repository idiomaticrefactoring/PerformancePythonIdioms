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
    bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/remain_code/prefined_cpus_remain_code/"

    bench_time_info_dir_list=["remain_code/prefined_cpus_remain_code",
        "code_time_info_prefined_cpu",
                              "code_base/code_time_info"]#code_base
    bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/code/code_base/"#code/

    # remain_dir=util.data_root + "lab_performance/list_compre_benchmarks/prefined_cpus_remain_code/"
    # util.mkdirs(remain_dir)

    for dir_e in bench_time_info_dir_list[:1]:
        bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/"+dir_e+"/"
        # print(dir_e)
        print(f"total file of benchmarks in {bench_time_info_dir} is: ", len(os.listdir(bench_time_info_dir)))
        total_unstable_count = 0
        total_unstable_invo_count=0
        total_idiom_unstable_count = 0
        file_name_list=[]
        # continue
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
            # file_unstable_count=0
            # file_idiom_unstable_count=0
            # if ind>10:
            #     break
            # if file_name!="2_4_3_[1].pkl":#"1_1_0_list(range(1,11))*10.pkl":#
            #     continue
            print("file_name: ",file_name)
            file_name_no_suffix = file_name[:-4]
            lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
            lab_code_info: LabCodeInfo
            print(lab_code_info.get_performance_info(warms_up=3, window=4))
            print(lab_code_info.get_features())
            break
            '''
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
            valid_time_list = lab_performance_util.get_time_list_within_cov(time_list,window)
            idiom_time_list = [[float(e) for e in e_list[warms_up:]] for e_list in idiom_time_list]
            valid_idiom_time_list = lab_performance_util.get_time_list_within_cov(idiom_time_list, window)
            if len(valid_idiom_time_list)<10:
                print("the number of invocations of the benchmark  is less than 10:", len(valid_time_list))
            else:
                # print("len: ",len(valid_time_list))
                pass
            if len(valid_time_list)<10:
                total_unstable_count+=1
                print("the number of invocations of the benchmark  is less than 10:", len(valid_time_list))
            else:

                # print("len: ", len(valid_time_list))
                pass
            real_per_change = sum([sum(e) for e in valid_time_list])/sum([sum(e) for e in valid_idiom_time_list])

            all_boot_time_list=lab_performance_util.num_bootstrap(valid_time_list, steps=1000)
            all_boot_idiom_time_list=lab_performance_util.num_bootstrap(valid_idiom_time_list, steps=1000)

            
            #get performance change and confidence interval

            prf_change_list=[]
            for ind_step,boot_time_list in enumerate(all_boot_time_list):
                boot_idiom_time_list=all_boot_idiom_time_list[ind_step]
                e_sum = sum([sum(e) for e in boot_time_list])
                e_idiom_sum = sum([sum(e) for e in boot_idiom_time_list])
                # print("e_time_list: ",sum(e_time_list))
                # print(e_idiom_time_list)
                # print(np.mean(np.array(e_time_list,dtype=np.float64),None))
                per_change = e_sum / e_idiom_sum
                prf_change_list.append(per_change-real_per_change)
            left, right = np.percentile(prf_change_list, [2.5, 97.5])
            if left+real_per_change < 1 < right+real_per_change:
                print("file_name: ", file_name)
                print(left+real_per_change, right+real_per_change,real_per_change)
            else:
                # print("file_name: ", file_name)
                # print(left+real_per_change, right+real_per_change,real_per_change)
                pass
            '''
            # lab_performance_util.whether_all_invocations_stable(valid_time_list)
            # lab_performance_util.whether_all_invocations_stable(valid_idiom_time_list)


                # print(f"{file_name} don't reach stable in {ind_t+1} invocations")
            # if valid_count_invoca<10:
            #     print(f"{file_name} don't reach stable within 30 invocations")
            # if file_unstable_count:
            #     # print(f"{file_name} don't reach stable with {file_unstable_count} invocations")
            #     total_unstable_count+=1
            #     total_unstable_invo_count+=file_unstable_count
            #     file_name_list.append(file_name[:-4]+".py")

        # print("total_unstable_count,total_unstable_invo_count: ",total_unstable_count,total_idiom_unstable_count)
        # print("total count of unstable files: ",len(file_name_list),len(set(file_name_list)))
        # util.save_json(remain_dir,"prefined_cpus_remain_unstable",file_name_list)
        # file_name_list=util.load_json(remain_dir,"prefined_cpus_remain_unstable")
        # print("file_name_list: ",len(file_name_list),file_name_list[0])
            # print("time_list: ",np.mean(time_list),np.std(time_list),np.std(time_list)/np.mean(time_list))
            # print("idiom_time_list: ",np.mean(idiom_time_list),np.std(idiom_time_list),np.std(idiom_time_list)/np.mean(idiom_time_list))

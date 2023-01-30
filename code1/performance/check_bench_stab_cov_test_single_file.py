import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)

import util,performance_util
from code_info import CodeInfo
'''
# return dict_flag_stable each ele is stable flag in all instances of all test methods 
'''
def get_flag(time_dict):

    dict_flag_stable = dict()
    for i, e_invo in enumerate(time_dict):
        # print(e_invo)

        for test_me in e_invo:
            # if ('https://github.com/kellyjonbrazil/jc/tree/master/tests/test_csv.py', 'tests.test_csv', 'MyTests', 'test_csv_flyrna') !=test_me:
            #     continue
            # print("the file: ",test_me,e_invo[test_me])
            if test_me not in dict_flag_stable:
                dict_flag_stable[test_me] = dict()
            for ind_case, test_case_time in enumerate(e_invo[test_me]):
                # print(test_case_time)
                test_case_time = [float(e) for e in test_case_time]
                stable_flag = performance_util.whether_cov(test_case_time[3:], window)
                if ind_case not in dict_flag_stable[test_me]:
                    dict_flag_stable[test_me][ind_case] = 0
                dict_flag_stable[test_me][ind_case] += stable_flag
        # break
    print(dict_flag_stable)

if __name__ == '__main__':
    #code_time_info_no_isolated code_time_info_prefined_cpu
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_perf_change/"
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_new_test_single_file_2/"
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_iter_improv_final_add_perf_change/"
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test/"
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_2/"
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_20invo/"
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_20invo_2/"
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_30invo/"
    save_code_info_dir_add_performance_change=util.data_root+"performance/list_compre_benchmarks_iter_improv_final_add_perf_change_test_30invo_2/"


    bench_time_info_dir_list=["performance/list_compre_benchmarks_iter_improv_final_test_30invo_2/"
        ,"performance/list_compre_benchmarks_iter_improv_final_test_30invo/",
        "performance/list_compre_benchmarks_iter_improv_final_test_20invo_2/","performance/list_compre_benchmarks_iter_improv_final_test_20invo/","performance/list_compre_benchmarks_iter_improv_final_test_2/","performance/list_compre_benchmarks_iter_improv_final_test/","performance/list_compre_benchmarks_iter_improv_final/","performance/list_compre_benchmarks_new_test_single_file_final/","performance/list_compre_benchmarks_new/","performance/list_compre_benchmarks/"]#code_base
    file_name_stable_list=[]
    file_name_list=set([])
    total_code_num=0
    total_code_instance_num=0
    total_code_stable_num=0
    total_code_instance_stable_num=0

    total_code_stable_num_pythonic = 0
    total_code_instance_stable_num_pythonic = 0
    both_total_code_stable_num=0
    both_total_code_instance_stable_num=0
    num_ele_num_dict=dict()
    window=4
    for dir_e in bench_time_info_dir_list[:1]:
        bench_time_info_dir=util.data_root+dir_e
        # print(dir_e)
        print(f"total file of benchmarks in {bench_time_info_dir} is: ", len(os.listdir(bench_time_info_dir)))
        # file_name_list=[]
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
            # print("file_name: ",file_name)
            # break
            file_name_list.add(file_name)
            if file_name in file_name_stable_list:
                continue
            # if ind>10:
            #     break
            # if file_name!="2_4_3_[1].pkl":#"1_1_0_list(range(1,11))*10.pkl":#
            #     continue
            file_name_no_suffix = file_name[:-4]
            lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
            lab_code_info: CodeInfo
            # if lab_code_info.file_html!="https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv.py":
            #     continue
            # time_dict=lab_code_info.compli_code_time_dict#lab_code_info.simple_code_time_dict
            # get_flag(time_dict)
            # get_flag(lab_code_info.simple_code_time_dict)
            # flag_test_html=lab_code_info.flag_total_test_html_pythonic#lab_code_info.flag_total_test_html
            #
            # print(flag_test_html)
            # print(lab_code_info.flag_total_test_html)
            # print(len(lab_code_info.simple_code_time_dict))
            # print("**********************************")
            # print(len(lab_code_info.compli_code_time_dict))
            # print("**********************************")
            # print(lab_code_info.num_ele_list)
            # print("**********************************")
            # print(lab_code_info.size_obj_dict)
            stable_info_dict=lab_code_info.get_stable_info_dict()
            # num_stable,num_instance=0,0
            # for test_me in stable_info_dict:
            #     for instance in stable_info_dict[test_me]:
            #         num_stable+=1
            #         num_ele=lab_code_info.num_ele_list[test_me][instance][0]
            #         if num_ele not in num_ele_num_dict:
            #             num_ele_num_dict[num_ele]=1
            #         else:
            #             num_ele_num_dict[num_ele] +=1
            # print("num_stable: ",num_stable)
            # both_total_code_instance_stable_num+=num_stable
            # print("stable_info_dict: ", stable_info_dict)
            total_time_list_info_dict=lab_code_info.get_stable_time_list(stable_info_dict=stable_info_dict)
            # print("total_time_list_info_dict: ",total_time_list_info_dict)
            lab_code_info.get_performance_info(total_time_list_info_dict=total_time_list_info_dict)
            '''
            warms_up=3
            window=4
            stable_info_dict =dict()
            total_code_num += 1
            flag_stable = 1
            flag_stable_pythonic = 1
            both_flag_stable = 1
            for test_me in lab_code_info.flag_total_test_html_instances:
                instance_list = lab_code_info.flag_total_test_html_instances[test_me]
                instance_list_pythonic = lab_code_info.flag_total_test_html_instances_pythonic[test_me]

                for instance in instance_list:
                    total_code_instance_num += 1
                    if instance_list[instance] >= 10:
                        total_code_instance_stable_num += 1
                    else:
                        flag_stable = 0
                        both_flag_stable = 0
                    if instance not in instance_list_pythonic:
                        print("why instance not in instance_list_pythonic: ", instance, "\n", instance_list[instance],
                              instance_list_pythonic)
                    if instance in instance_list_pythonic and instance_list_pythonic[instance] >= 10:
                        total_code_instance_stable_num_pythonic += 1
                    else:
                        flag_stable_pythonic = 0
                        both_flag_stable = 0
                    if instance in instance_list_pythonic and instance_list_pythonic[instance] >= 10 and instance_list[
                        instance] >= 10:
                        both_total_code_instance_stable_num += 1
                        if test_me not in stable_info_dict:
                            stable_info_dict[test_me] = [instance]
                        else:
                            stable_info_dict[test_me].append(instance)

            if flag_stable:
                total_code_stable_num += 1
            if flag_stable_pythonic:
                total_code_stable_num_pythonic += 1
            if both_flag_stable:
                both_total_code_stable_num += 1


            compli_code_time_list=lab_code_info.compli_code_time_dict
            simple_code_time_list=lab_code_info.simple_code_time_dict
            # num_add_ele_dict=lab_code_info.num_ele_list
            total_time_list_info_dict=dict()
            for ind_invo, each_compli_code_time_dict in enumerate(compli_code_time_list):
                for test_me in each_compli_code_time_dict:
                    if test_me in stable_info_dict:
                        for ind_instance,instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
                            if ind_instance in stable_info_dict[test_me]:
                                if test_me not in total_time_list_info_dict:
                                    total_time_list_info_dict[test_me]=dict()
                                if ind_instance not in total_time_list_info_dict[test_me]:
                                    total_time_list_info_dict[test_me][ind_instance] ={"time_list":[],"num_ele":None,"pythonic_time_list":[]}
                                steady_time_list = [float(e) for e in instance_time_list[warms_up:]]
                                valid_time_list = performance_util.get_time_list_within_cov(steady_time_list, window)
                                if valid_time_list:
                                    total_time_list_info_dict[test_me][ind_instance]["time_list"].append(valid_time_list)

                                instance_time_list_pythonic = simple_code_time_list[ind_invo][test_me][ind_instance]
                                steady_time_list = [float(e) for e in instance_time_list_pythonic[warms_up:]]
                                valid_time_list = performance_util.get_time_list_within_cov(steady_time_list, window)
                                if valid_time_list:
                                    total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"].append(
                                        valid_time_list)
                                # total_time_list_info_dict[test_me][ind_instance]["num_ele"]=int(num_add_ele_dict[test_me][ind_instance][0])

            for test_me in total_time_list_info_dict:
                for ind_instance in total_time_list_info_dict[test_me]:
                    valid_time_list=total_time_list_info_dict[test_me][ind_instance]["time_list"]
                    valid_idiom_time_list=total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"]
                    if len(valid_time_list)<10 or len(valid_idiom_time_list)<10:
                        print(f"check time list of {ind_instance}th of {test_me} because its stable invocations is less than 10 ",len(valid_time_list),len(valid_idiom_time_list))
                        continue
                    # print("valid_time_list,valid_idiom_time_list: ",valid_time_list,valid_idiom_time_list)
                    real_per_change = sum([sum(e) for e in valid_time_list]) / sum(
                        [sum(e) for e in valid_idiom_time_list])

                    all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=1000)
                    all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=1000)

                    
                    #get performance change and confidence interval
                    
                    prf_change_list = []
                    for ind_step, boot_time_list in enumerate(all_boot_time_list):
                        boot_idiom_time_list = all_boot_idiom_time_list[ind_step]
                        e_sum = sum([sum(e) for e in boot_time_list])
                        e_idiom_sum = sum([sum(e) for e in boot_idiom_time_list])
                        # print("e_time_list: ",sum(e_time_list))
                        # print(e_idiom_time_list)
                        # print(np.mean(np.array(e_time_list,dtype=np.float64),None))
                        per_change = e_sum / e_idiom_sum
                        prf_change_list.append(per_change - real_per_change)
                    left, right = np.percentile(prf_change_list, [2.5, 97.5])
                    mean_perf_change = real_per_change
                    if left + real_per_change < 1 < right + real_per_change:
                        # print("file_name: ", self.file_path.split("/")[-1])
                        print(left + real_per_change, right + real_per_change, real_per_change)
                        mean_perf_change = 1.0
                    else:
                        # print("file_name: ", file_name)
                        # print(left+real_per_change, right+real_per_change,real_per_change)
                        pass
                    stable_compli_time_list = valid_time_list
                    stable_simp_time = valid_idiom_time_list
                    interval = (left, right)
                    print(f"{ind_instance}th instance of {test_me} test method's  performance change info: ",real_per_change,(left+real_per_change, right+real_per_change))

            '''

            # break
            # print("",lab_code_info.)
            # print("flag_total_test_html: ",lab_code_info.flag_total_test_html)


            '''
            print("flag_total_test_html_instances: ",lab_code_info.flag_total_test_html_instances)
            print("*************************************")
            # print("flag_total_test_html_pythonic: ",lab_code_info.flag_total_test_html_pythonic)
            print("flag_total_test_html_instances_pythonic: ",lab_code_info.flag_total_test_html_instances_pythonic)
            '''
            # print("performance change: ",lab_code_info.total_time_list_info_dict)
            util.save_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix, lab_code_info)
            # lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
            # print(">>>test load info>>>>>>>performance change: ",lab_code_info.total_time_list_info_dict)

            # break
    print("num_ele_num_dict: ",num_ele_num_dict)
    '''
    {'119': 2, '2': 106, '1': 249, '87': 1, '18': 2, '11766': 1, '128': 1, '16': 5, '4': 13, '0': 84, '8': 15, '3': 44, '6': 14, '26': 1, '5': 52, '101': 1, '100': 2, '10': 16, '7': 2, '11': 1, '246': 1, '127': 1, '91': 1, '24': 1, '17': 1, '30': 1, '9': 1, '31': 2}
    '''
    print(f"stable info:\ntotal_code_num: {total_code_num}, total_code_instance_num: {total_code_instance_num}\n"
          f"both_total_code_stable_num: {both_total_code_stable_num}, both_total_code_instance_stable_num: {both_total_code_instance_stable_num}\n"
          f"total_code_stable_num: {total_code_stable_num}, total_code_instance_stable_num: {total_code_instance_stable_num}\n"
          f"total_code_stable_num_pythonic: {total_code_stable_num_pythonic}, total_code_instance_stable_num_pythonic: {total_code_instance_stable_num_pythonic}")

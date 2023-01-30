import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
sys.path.append(code_dir+"lab_performance")
sys.path.append(code_dir+"wrap_refactoring/")
from for_else import performance_replace_content_by_ast_for_else

import refactor_for_else
import lab_performance_util
import util
from lab_code_info import LabCodeInfo
'''
1. for all non-idiomatic code, refactor them into idiomatic code
2. record time for non-idiomatic code
    2.1 insert time.per_counter() and iterations to generate new non-idiomatic code
    2.2 run the file  to get time_list
3 record time for idiomatic code
    3.1 
'''



def save_one_file_time_list(file_name, code_list):
    for ind, (old_tree, new_tree, break_list_in_for, child, child_copy, \
        ass_init, if_varnode, init_ass_remove_flag) in enumerate(code_list):
        # old_tree = arg_list[0]
        # call_node = arg_list[-2]
        file_path = bench_dir + file_name
        # if os.path.exists(bench_time_info_dir + file_name[:-3] + ".pkl"):
        #     continue
        if 1:
            old_content, new_content, flag_same = performance_replace_content_by_ast_for_else.replace_content_for_else_insert_time_simple(
                file_path, child, child_copy, ass_init, if_varnode, init_ass_remove_flag)

            '''
            print("old_content: ")
            print(old_content)
            print("new_content: ")
            print(new_content)
            '''
            new_add_iterations_content = lab_performance_util.insert_iterations_for_else(new_content, iterations)

            # print("new_add_iterations_content: ")
            # print(new_add_iterations_content)
            '''
            print(">>>>>>>>>>>>>>>>whether timing new content and old content is same: ", flag_same)
            '''
            util.save_file_path(time_complicate_bench_dir + file_name, new_add_iterations_content)
        if 1:  # not os.path.exists(time_simp_bench_dir + file_name):
            old_content, new_content, flag_same = performance_replace_content_by_ast_for_else.replace_content_for_else_simple(
                file_path, child, child_copy, ass_init, if_varnode, init_ass_remove_flag)
            # print("new_content: ")

            # '''
            new_add_iterations_content = lab_performance_util.insert_iterations_for_else(new_content, iterations)
            # print("pythonic new_add_iterations_content: ")
            # print(new_add_iterations_content)
            util.save_file_path(time_simp_bench_dir + file_name, new_add_iterations_content)
        # break
        all_time_list = []
        all_pythonic_time_list = []
        num_add_ele = None
        stable_invo = 0
        for invo in range(invocations):
            output = lab_performance_util.sequence_run(time_complicate_bench_dir, file_name, invo=invo,
                                                       log_dir=log_time_complicate_bench_dir,
                                                       prefined_cpu=prefined_cpu)
            get_time_list = lab_performance_util.get_time_list(output)
            # time_list = [float(e) for e in get_time_list[warms_up:]]
            # stable_flag = lab_performance_util.whether_cov(time_list, window)
            # stable_invo += stable_flag

            all_time_list.append(get_time_list)
            # print("get_time_list: ", get_time_list)
            # break

                # print("num_add_ele: ",num_add_ele)
        stable_invo_idiom = 0
        for invo in range(invocations):
            output = lab_performance_util.sequence_run(time_simp_bench_dir, file_name, invo=invo,
                                                       log_dir=log_time_simp_bench_dir,
                                                       prefined_cpu=prefined_cpu
                                                       )
            get_pythonic_time_list = lab_performance_util.get_pythonic_time_list(output)
            # time_list = [float(e) for e in get_pythonic_time_list[warms_up:]]
            # stable_flag = lab_performance_util.whether_cov(time_list, window)
            # stable_invo_idiom += stable_flag
            all_pythonic_time_list.append(get_pythonic_time_list)
            # print("get_pythonic_time_list: ", get_pythonic_time_list)
            # break
            # if stable_invo_idiom >= thresh_invo:
            #     print(file_name, " simple code is stable when invocations are : ", invo + 1)
            #     break
            # print(get_pythonic_time_list)
        # print("num_add_ele: ", num_add_ele)
        print("len of all_time_list: ", len(all_time_list), len(all_pythonic_time_list))
        # print("all_time_list: ", all_time_list)
        lab_code = LabCodeInfo(bench_dir, file_name, code_info=[old_tree, new_tree],
                               idiomatic_path=time_simp_bench_dir + file_name,
                               non_idiomatic_path=time_complicate_bench_dir + file_name,
                               compli_code_time_list=all_time_list, simple_code_time_list=all_pythonic_time_list,
                               num_add_ele=num_add_ele, iterations=iterations, invocations=invocations)
        util.save_pkl(bench_time_info_dir, file_name[:-3], lab_code)

        # '''
        # lab_code_info=util.load_pkl(bench_time_info_dir, file_name[:-3])
        # print(lab_code_info)
        # print(lab_code_info.code_info)
        print("save time for file has finished! ", bench_time_info_dir + file_name)
    print("one file time: ", time.time() - time_start)
if __name__ == '__main__':
    # iterations = 35
    # invocations = 50
    # thresh_invo = 50
    iterations = 35
    invocations = 50
    thresh_invo = 50
    # iterations=20
    # invocations=30
    warms_up=3
    window=4
    pro_time_start = time.time()
    log_time_complicate_bench_dir_old = util.data_root_mv + "lab_performance/for_else_benchmarks/log/log_time_compli_code_prefined_cpu_new/"
    log_time_complicate_bench_dir = util.data_root_mv + "lab_performance/for_else_benchmarks_paper/log/log_time_compli_code_prefined_cpu_new/"

    # log_time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/log/log_time_list_compreh_compli_code/"
    log_time_simp_bench_dir_old = util.data_root_mv + "lab_performance/for_else_benchmarks/log/log_time_simp_code_prefined_cpu_new/"
    log_time_simp_bench_dir = util.data_root_mv + "lab_performance/for_else_benchmarks_paper/log/log_time_simp_code_prefined_cpu_new/"

    # util.mkdirs(log_time_complicate_bench_dir)
    # util.mkdirs(log_time_simp_bench_dir)
    # time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/code/time_complicated_code/"
    time_complicate_bench_dir_old = util.data_root_mv + "lab_performance/for_else_benchmarks/code/time_complicated_code_prefined_cpu_new/"
    time_complicate_bench_dir = util.data_root_mv + "lab_performance/for_else_benchmarks_paper/code/time_complicated_code_prefined_cpu_new/"

    time_simp_bench_dir_old = util.data_root_mv + "lab_performance/for_else_benchmarks/code/time_simple_code_prefined_cpu_new/"
    time_simp_bench_dir = util.data_root_mv + "lab_performance/for_else_benchmarks_paper/code/time_simple_code_prefined_cpu_new/"

    # util.mkdirs(time_complicate_bench_dir)
    # util.mkdirs(time_simp_bench_dir)
    bench_time_info_dir_old=util.data_root_mv + "lab_performance/for_else_benchmarks/bench_time_info_dir_prefined_cpu_new/"
    bench_time_info_dir=util.data_root_mv + "lab_performance/for_else_benchmarks_paper/bench_time_info_dir_prefined_cpu_new/"

    util.mkdirs(bench_time_info_dir)

    bench_dir_old = util.data_root_mv + "lab_performance/for_else_benchmarks/code/code/"
    bench_dir = util.data_root_mv + "lab_performance/for_else_benchmarks_paper/code/code/"

    total_start_time=time.time()
    prefined_cpu = "taskset -c 2,3 "
    print("total number: ",len(os.listdir(bench_dir)))
    import random
    dir_list=list(os.listdir(bench_dir))
    dir_list.sort()
    # remain_dir=util.data_root + "lab_performance/list_compre_benchmarks/prefined_cpus_remain_code_2/"
    #
    # # remain_dir=util.data_root + "lab_performance/list_compre_benchmarks/prefined_cpus_remain_code_1/"
    # dir_list = util.load_json(remain_dir, "prefined_cpus_remain_unstable")
    random.seed(2022)
    random.shuffle(dir_list)
    # print(len(dir_list))
    import shutil
    # filter_file_name_list=["list(range(1,10000001))"]#["1_0_0_[]_func.py","1_0_0_[1]_func.py","1_0_0_list(range(1,11))_func.py","1_0_0_list(range(1,101))_func.py","1_0_0_list(range(1,1001))_func.py","1_0_0_list(range(1,10001))_func.py"]
    count_remain=0
    offset=0
    end=128
    for ind,file_name in enumerate(dir_list[offset:end]):#9001750
        # if "1000000" in file_name:
        #     continue

        # if ind>3:
        #     break
        # if file_name!="5_ass_const_func.py":#"6_ass_swap_func.py":
        #     continue
        if os.path.exists(bench_time_info_dir_old + file_name[:-3] + ".pkl"):
            print(bench_time_info_dir + file_name, "is existed")
            shutil.copyfile(bench_time_info_dir_old+ file_name[:-3] + ".pkl",bench_time_info_dir+ file_name[:-3] + ".pkl")
            continue
        count_remain+=1
        # continue
        #'''
        # break
        # if file_name=="2_3_0_list(range(1,11))*1000.py":
        #     continue

        # if file_name in filter_file_name_list:#!="1_0_0_list(range(1,100001))_func.py":#"1_1_0_list(range(1,11))*10.py":##"4_0_0_[1].py":#"1_1_0_list(range(1,11))*10.py":
        #     continue

        time_start = time.time()
        print(">>>>come file: ", file_name)
        # continue
        if '.py' not in file_name:
            continue
        code_list = refactor_for_else.refactor_for_else(bench_dir + file_name)
#                        code_list.append([tree,tree_copy,break_list_in_for,child,child_copy,intersect_infor_ass_init[0][1],if_varnode,init_ass_remove_flag])
#         break
        # continue
        # for code in code_list:
        #     print("code: ",code)
        code_list=[code_list[-1]]
        if len(code_list) > 1:
            print("the file has errors, please check! ", bench_dir + file_name)
            continue
        # continue
        # for ind, (old_tree, new_tree) in enumerate(code_list):
        #     file_path = bench_dir + file_name
        #     # if os.path.exists(bench_time_info_dir+file_name[:-3]+".pkl"):
        #     #     continue
        #     count_remain+=1
        # print("code_list: ",code_list)

        save_one_file_time_list(file_name, code_list)
        # break
        #'''
    print("count_remain: ", count_remain)


    total_end_time = time.time()
    print("total time: ", total_end_time - total_start_time)

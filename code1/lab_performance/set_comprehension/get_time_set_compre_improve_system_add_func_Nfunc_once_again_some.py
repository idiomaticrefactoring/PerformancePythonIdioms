import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_set_comprehension
import performance_replace_content_by_ast_time_percounter
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


def save_one_file_time_list(file_name, code_list,invocations,iterations):
    for ind, (for_node, assign_node, remove_ass_flag, new_tree) in enumerate(code_list):
        file_path = bench_dir + file_name
        # if os.path.exists(bench_time_info_dir + file_name[:-3] + ".pkl"):
        #     continue
        if 1:  # not os.path.exists(time_complicate_bench_dir+file_name):
            old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category_insert_time_complete(
                file_path, for_node,
                assign_node,
                new_tree, remove_ass_flag)
            '''
            print("old_content: ")
            print(old_content)
            print("new_content: ")
            print(new_content)
            '''
            new_add_iterations_content = lab_performance_util.insert_iterations(new_content, iterations)
            #'''
            # print("new_add_iterations_content: ")
            print(new_add_iterations_content)
            # print(">>>>>>>>>>>>>>>>whether timing new content and old content is same: ", flag_same)
            #'''
            util.save_file_path(time_complicate_bench_dir + file_name, new_add_iterations_content)
        if 1:  # not os.path.exists(time_simp_bench_dir + file_name):
            old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category(
                file_path, for_node,
                assign_node,
                new_tree, remove_ass_flag)
            # print("new_content: ")
            # print(new_content)
            # '''
            new_add_iterations_content = lab_performance_util.insert_iterations(new_content, iterations)
            # print("new_add_iterations_content: ")
            print(new_add_iterations_content)
            # print(">>>>>>>>>>>>>>>>whether timing new content and old content is same: ", flag_same)
            util.save_file_path(time_simp_bench_dir + file_name, new_add_iterations_content)
        #'''
        all_time_list = []
        all_pythonic_time_list = []
        num_add_ele = None
        stable_invo = 0
        for invo in range(invocations):
            output = lab_performance_util.sequence_run(time_complicate_bench_dir, file_name, invo=invo,
                                                       log_dir=log_time_complicate_bench_dir + file_name[:-3] + "/",
                                                       prefined_cpu=prefined_cpu)
            each_all_time_list = lab_performance_util.get_time_list(output)
            time_list = [float(e) for e in each_all_time_list[warms_up:]]
            stable_flag = lab_performance_util.whether_cov(time_list, window)
            stable_invo += stable_flag

            all_time_list.append(each_all_time_list)
            if invo == 0:
                # print(get_time_list)
                num_add_ele = lab_performance_util.get_num_add_ele(output)
            # if stable_invo >= thresh_invo:
            #     print(file_name, " complicated code is stable when invocations are : ", invo + 1)
            #     break

                # print("num_add_ele: ",num_add_ele)
        stable_invo_idiom = 0
        for invo in range(invocations):
            output = lab_performance_util.sequence_run(time_simp_bench_dir, file_name, invo=invo,
                                                       log_dir=log_time_simp_bench_dir + file_name[:-3] + "/",
                                                       prefined_cpu=prefined_cpu
                                                       )
            pythonic_time_list = lab_performance_util.get_pythonic_time_list(output)
            time_list = [float(e) for e in pythonic_time_list[warms_up:]]
            stable_flag = lab_performance_util.whether_cov(time_list, window)
            stable_invo_idiom += stable_flag
            all_pythonic_time_list.append(pythonic_time_list)
            # if stable_invo_idiom >= thresh_invo:
            #     print(file_name, " simple code is stable when invocations are : ", invo + 1)
            #     break
            # print(get_pythonic_time_list)
        print("num_add_ele: ", num_add_ele)
        print("len of all_time_list: ", len(all_time_list), len(all_pythonic_time_list))
        # print("all_time_list: ", all_time_list)
        lab_code = LabCodeInfo(bench_dir, file_name, code_info=[for_node, assign_node, remove_ass_flag, new_tree],
                               idiomatic_path=time_simp_bench_dir + file_name,
                               non_idiomatic_path=time_complicate_bench_dir + file_name,
                               compli_code_time_list=all_time_list, simple_code_time_list=all_pythonic_time_list,
                               num_add_ele=num_add_ele, iterations=iterations, invocations=invocations)
        util.save_pkl(bench_time_info_dir, file_name[:-3], lab_code)

        #'''
        # lab_code_info=util.load_pkl(bench_time_info_dir, file_name[:-3])
        # print(lab_code_info)
        # print(lab_code_info.code_info)
        print("save time for file has finished! ", bench_time_info_dir + file_name)
    print("one file time: ", time.time() - time_start)
if __name__ == '__main__':
    iterations = 300#35
    invocations = 50
    thresh_invo = 50
    # iterations=20
    # invocations=30
    warms_up=3
    window=4
    pro_time_start = time.time()
    log_time_complicate_bench_dir = util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/log/log_time_compli_code_prefined_cpu_new/"
    # log_time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/log/log_time_list_compreh_compli_code/"
    log_time_simp_bench_dir = util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/log/log_time_simp_code_prefined_cpu_new/"
    # util.mkdirs(log_time_complicate_bench_dir)
    # util.mkdirs(log_time_simp_bench_dir)
    # time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/code/time_complicated_code/"
    time_complicate_bench_dir = util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/code/time_complicated_code_prefined_cpu_new/"
    time_simp_bench_dir = util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/code/time_simple_code_prefined_cpu_new/"

    # util.mkdirs(time_complicate_bench_dir)
    # util.mkdirs(time_simp_bench_dir)
    bench_time_info_dir=util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/prefined_cpus_remain_code_new/"
    # util.mkdirs(bench_time_info_dir)
    bench_dir = util.data_root_mv + "lab_performance/set_compre_benchmarks/code/code/"
    total_start_time=time.time()
    prefined_cpu = "taskset -c 2,3  "#"taskset -c 7 "#"taskset -c 2,3 "
    print("total number: ",len(os.listdir(bench_dir)))
    import random
    dir_list=list(os.listdir(bench_dir))
    dir_list.sort()
    # print(dir_list)
    # dir_list=["1_2_0_list(range(1,10000001))_func.py"]
    # remain_dir=util.data_root + "lab_performance/list_compre_benchmarks/prefined_cpus_remain_code_2/"
    #
    # # remain_dir=util.data_root + "lab_performance/list_compre_benchmarks/prefined_cpus_remain_code_1/"
    # dir_list = util.load_json(remain_dir, "prefined_cpus_remain_unstable")
    random.seed(2022)
    random.shuffle(dir_list)
    # print(len(dir_list))
    filter_file_name_list = ["list(range(1,10000001))", 'list(range(1,3163))',
                             'list(range(1,216))', 'list(range(1,57))']
    filter_file_name_list =['list(range(1,1000001))','list(range(1,1001))','list(range(1,100001))','list(range(1,101))','list(range(1,33))']
    filter_file_name_list = ['list(range(1,1000001))', 'list(range(1,1001))', 'list(range(1,101))', 'list(range(1,33))',"list(range(1,317))"]
    once_again_file_name_list=['1_0_0_list(range(1,1000001)).py', '1_0_0_list(range(1,1000001))_func.py', '1_0_0_list(range(1,100001)).py',
     '1_0_0_list(range(1,100001))_func.py', '1_0_0_list(range(1,10001)).py', '1_0_0_list(range(1,10001))_func.py',
     '1_0_0_list(range(1,1001)).py', '1_0_0_list(range(1,1001))_func.py', '1_0_0_list(range(1,101)).py',
     '1_0_0_list(range(1,101))_func.py', '1_0_0_list(range(1,11)).py', '1_0_1_list(range(1,1000001)).py',
     '1_0_1_list(range(1,1000001))_func.py', '1_0_1_list(range(1,100001)).py', '1_0_1_list(range(1,100001))_func.py',
     '1_0_1_list(range(1,10001)).py', '1_0_1_list(range(1,1001)).py', '1_0_1_list(range(1,101)).py',
     '1_0_2_list(range(1,1000001)).py', '1_0_2_list(range(1,1000001))_func.py', '1_0_2_list(range(1,100001)).py',
     '1_0_2_list(range(1,10001)).py', '1_0_2_list(range(1,1001)).py', '1_0_2_list(range(1,101)).py',
     '1_0_3_list(range(1,1000001)).py', '1_0_3_list(range(1,100001)).py', '1_0_3_list(range(1,10001)).py',
     '1_0_4_list(range(1,1000001)).py', '1_0_4_list(range(1,100001)).py', '1_0_4_list(range(1,10001)).py',
     '1_0_4_list(range(1,1001)).py', '1_1_0_list(range(1,1000001)).py', '1_1_0_list(range(1,1000001))_func.py',
     '1_1_0_list(range(1,100001)).py', '1_1_0_list(range(1,10001)).py', '1_1_0_list(range(1,1001)).py',
     '1_1_0_list(range(1,101)).py', '1_1_1_list(range(1,1000001)).py', '1_1_1_list(range(1,100001)).py',
     '1_1_1_list(range(1,10001)).py', '1_1_1_list(range(1,1001)).py', '1_1_1_list(range(1,101)).py',
     '1_1_2_list(range(1,1000001)).py', '1_1_2_list(range(1,100001)).py', '1_1_2_list(range(1,10001)).py',
     '1_1_2_list(range(1,1001)).py', '1_1_2_list(range(1,101)).py', '1_1_3_list(range(1,1000001)).py',
     '1_1_3_list(range(1,100001)).py', '1_1_4_list(range(1,1000001)).py', '1_1_4_list(range(1,10001)).py',
     '1_2_0_list(range(1,1000001)).py', '1_2_0_list(range(1,10001)).py', '1_2_0_list(range(1,101)).py',
     '1_2_1_list(range(1,1000001)).py', '1_2_1_list(range(1,100001)).py', '1_2_1_list(range(1,101)).py',
     '1_2_2_list(range(1,1000001)).py', '1_2_2_list(range(1,100001)).py', '1_2_2_list(range(1,101)).py',
     '2_0_0_list(range(1,1001)).py', '2_0_0_list(range(1,101)).py', '2_0_0_list(range(1,11)).py',
     '2_0_0_list(range(1,317)).py', '2_0_0_list(range(1,317))_func.py', '2_0_0_list(range(1,33)).py',
     '2_0_1_list(range(1,1001)).py', '2_0_1_list(range(1,101)).py', '2_0_1_list(range(1,11)).py',
     '2_0_1_list(range(1,317)).py', '2_0_1_list(range(1,33)).py', '2_0_2_list(range(1,1001)).py',
     '2_0_2_list(range(1,101)).py', '2_0_2_list(range(1,11)).py', '2_0_2_list(range(1,317)).py',
     '2_0_2_list(range(1,33)).py', '2_0_4_list(range(1,1001)).py', '2_1_0_list(range(1,1001)).py',
     '2_1_0_list(range(1,101)).py', '2_1_0_list(range(1,11)).py', '2_1_0_list(range(1,317)).py',
     '2_1_0_list(range(1,33)).py', '2_1_1_list(range(1,1001)).py', '2_1_1_list(range(1,317)).py',
     '2_1_1_list(range(1,33)).py', '2_1_2_list(range(1,1001)).py', '2_2_0_list(range(1,11)).py',
     '2_2_0_list(range(1,317)).py', '2_2_0_list(range(1,33)).py', '2_2_1_list(range(1,33)).py',
     '2_2_2_list(range(1,317)).py', '2_2_2_list(range(1,33)).py', '3_0_0_list(range(1,101)).py',
     '3_0_0_list(range(1,47)).py', '3_0_1_list(range(1,101)).py', '3_1_0_list(range(1,47)).py',
     '4_0_0_list(range(1,33)).py', '4_2_2_list(range(1,33)).py']
    once_again_file_name_list=['1_0_0_list(range(1,1000001)).py', '1_0_0_list(range(1,1000001))_func.py', '1_0_0_list(range(1,100001)).py',
     '1_0_0_list(range(1,100001))_func.py', '1_0_0_list(range(1,10001)).py', '1_0_0_list(range(1,10001))_func.py',
     '1_0_0_list(range(1,1001)).py', '1_0_0_list(range(1,1001))_func.py', '1_0_0_list(range(1,101)).py',
     '1_0_1_list(range(1,1000001)).py', '1_0_1_list(range(1,100001)).py', '1_0_2_list(range(1,1000001)).py',
     '1_1_0_list(range(1,1000001)).py']
    once_again_file_name_list = ["1_3_0_[].py","3_0_2_[].py"]
    once_again_file_name_list=['1_0_0_[1].py', '1_0_0_list(range(1,11))_func.py', '1_0_2_[1].py', '1_0_2_[].py',
     '1_0_2_list(range(1,101))_func.py', '1_0_2_list(range(1,11))_func.py', '1_0_3_[1]_func.py', '1_0_3_[]_func.py',
     '1_0_4_[1].py', '1_0_4_[1]_func.py', '1_0_4_[]_func.py', '1_0_4_list(range(1,100001))_func.py', '1_1_0_[].py',
     '1_1_0_[]_func.py', '1_1_0_list(range(1,1000001))_func.py', '1_1_0_list(range(1,1001)).py',
     '1_1_0_list(range(1,11)).py', '1_1_1_[1]_func.py', '1_1_1_[].py', '1_1_1_[]_func.py', '1_1_3_[].py',
     '1_1_3_list(range(1,11)).py', '1_1_4_[1].py', '1_1_4_[1]_func.py', '1_1_4_[].py', '1_2_0_[].py',
     '1_2_1_[]_func.py', '1_2_2_[]_func.py', '1_2_3_[]_func.py', '1_2_4_[].py', '1_3_0_[].py',
     '1_3_0_list(range(1,11)).py', '1_3_1_[1].py', '1_3_1_[].py', '1_3_1_[]_func.py', '1_3_1_list(range(1,1001)).py',
     '1_3_1_list(range(1,11))_func.py', '1_3_3_[].py', '1_3_3_[]_func.py', '1_3_4_[].py', '1_4_2_[]_func.py',
     '1_4_2_list(range(1,1001)).py', '1_4_3_[]_func.py', '1_4_4_[]_func.py', '2_0_0_[1].py', '2_0_0_[1]_func.py',
     '2_0_0_[]_func.py', '2_0_1_[]_func.py', '2_0_1_list(range(1,4))_func.py', '2_0_2_[].py', '2_0_2_[]_func.py',
     '2_0_2_list(range(1,4))_func.py', '2_0_3_[]_func.py', '2_0_4_list(range(1,11))_func.py',
     '2_1_0_list(range(1,1001)).py', '2_1_0_list(range(1,101))_func.py', '2_1_0_list(range(1,11)).py',
     '2_1_0_list(range(1,4))_func.py', '2_1_1_list(range(1,4)).py', '2_1_2_[1].py', '2_1_2_[].py', '2_1_2_[]_func.py',
     '2_1_2_list(range(1,1001)).py', '2_1_2_list(range(1,11))_func.py', '2_1_3_[1]_func.py',
     '2_1_3_list(range(1,33)).py', '2_1_4_[]_func.py', '2_1_4_list(range(1,4)).py', '2_2_0_[]_func.py',
     '2_2_0_list(range(1,4))_func.py', '2_2_1_[1].py', '2_2_1_[1]_func.py', '2_2_2_[1].py', '2_2_2_[]_func.py',
     '2_2_2_list(range(1,1001))_func.py', '2_2_3_[]_func.py', '2_2_3_list(range(1,4)).py',
     '2_2_4_list(range(1,4))_func.py', '2_3_0_[]_func.py', '2_3_0_list(range(1,1001)).py',
     '2_3_0_list(range(1,317))_func.py', '2_3_0_list(range(1,4)).py', '2_3_1_[1].py', '2_3_1_[1]_func.py',
     '2_3_1_[]_func.py', '2_3_1_list(range(1,4))_func.py', '2_3_2_[]_func.py', '2_3_3_[1]_func.py', '2_3_3_[]_func.py',
     '2_3_4_[].py', '2_3_4_[]_func.py', '2_3_4_list(range(1,4))_func.py', '2_4_0_[].py', '2_4_0_[]_func.py',
     '2_4_0_list(range(1,4))_func.py', '2_4_1_[]_func.py', '2_4_2_[1]_func.py', '2_4_2_[]_func.py', '2_4_3_[1].py',
     '2_4_4_[].py', '3_0_0_[]_func.py', '3_0_2_[].py', '3_0_2_[]_func.py', '3_0_2_list(range(1,3)).py', '3_0_3_[1].py',
     '3_0_3_[1]_func.py', '3_0_4_[].py', '3_1_0_list(range(1,11)).py', '3_1_0_list(range(1,3)).py', '3_1_1_[1]_func.py',
     '3_1_1_[]_func.py', '3_1_2_list(range(1,6))_func.py', '3_1_3_[1]_func.py', '3_1_3_list(range(1,3))_func.py',
     '3_1_4_[1].py', '3_1_4_[1]_func.py', '3_2_0_[1]_func.py', '3_2_0_[].py', '3_2_1_list(range(1,101))_func.py',
     '3_2_2_[1].py', '3_2_2_[].py', '3_3_0_[1].py', '3_3_0_[]_func.py', '3_3_1_[1].py', '3_3_1_[]_func.py',
     '3_3_2_[1].py', '3_3_2_[1]_func.py', '3_3_2_[]_func.py', '3_3_2_list(range(1,3))_func.py',
     '3_3_3_list(range(1,6)).py', '3_3_4_[]_func.py', '3_4_0_[1].py', '3_4_0_[1]_func.py', '3_4_1_[]_func.py',
     '3_4_1_list(range(1,101))_func.py', '3_4_1_list(range(1,3)).py', '3_4_2_[1]_func.py', '3_4_2_[]_func.py',
     '3_4_2_list(range(1,101)).py', '3_4_3_[]_func.py', '3_4_3_list(range(1,3))_func.py',
     '3_4_3_list(range(1,6))_func.py', '4_0_1_[].py', '4_0_1_[]_func.py', '4_0_1_list(range(1,3)).py',
     '4_0_1_list(range(1,4)).py', '4_0_2_[1].py', '4_0_2_[].py', '4_0_2_[]_func.py', '4_0_3_[]_func.py',
     '4_0_3_list(range(1,4)).py', '4_0_4_[]_func.py', '4_1_0_list(range(1,33)).py', '4_1_2_[1]_func.py', '4_1_3_[].py',
     '4_1_4_[].py', '4_2_0_list(range(1,4))_func.py', '4_2_1_[].py', '4_2_1_[]_func.py', '4_2_3_[1]_func.py',
     '4_2_3_[]_func.py', '4_3_0_[1]_func.py', '4_3_0_[].py', '4_3_1_[1].py', '4_3_2_[1].py',
     '4_3_2_list(range(1,3)).py', '4_3_2_list(range(1,3))_func.py', '4_3_3_[].py', '4_3_3_list(range(1,3))_func.py',
     '4_3_4_[].py', '4_4_0_[1].py', '4_4_0_[]_func.py', '4_4_1_[1].py', '4_4_1_[]_func.py',
     '4_4_1_list(range(1,4))_func.py', '4_4_4_list(range(1,3)).py']
    # filter_file_name = "list(range(1,10000001))"#900
    # filter_file_name_list=["1_0_0_[]_func.py","1_0_0_[1]_func.py","1_0_0_list(range(1,11))_func.py","1_0_0_list(range(1,101))_func.py","1_0_0_list(range(1,1001))_func.py","1_0_0_list(range(1,10001))_func.py"]
    count_remain=0
    offset=0
    end=533
    for file_name in dir_list[:]:
        invocations = 50
        # if "list(range(1,1000001))" not in file_name:
        #     continue
        if "3_0_2_[].py" != file_name:
            continue
        # if os.path.exists(bench_time_info_dir+ file_name[:-3] + ".pkl"):
        #     continue
        # print(file_name)
        if "[]" in file_name or "[1]" in file_name:
            iterations = 35  # 35
            invocations = 200
        else:
            iterations = 35  # 35
            invocations = 50
        flag_filter = 0
        for ind_filter,filter_file_name in enumerate(filter_file_name_list):
            if filter_file_name in file_name and file_name.startswith(f"{ind_filter+1}_"):
                flag_filter = 1
                break
                # continue
        if flag_filter:
            invocations=10
            continue
            # print("come here: ",file_name,invocations)
        # else:
        #     continue
            # continue
        # if "[1]" not in file_name:
        #     continue
        # if file_name not in once_again_file_name_list[58:116]:
        #     continue


        # continue
            # continue
        # if filter_file_name in file_name:
        #     # print("come here")
        #     continue
        # break
        # if file_name=="2_3_0_list(range(1,11))*1000.py":
        #     continue
        # if file_name in filter_file_name_list:#!="1_0_0_list(range(1,100001))_func.py":#"1_1_0_list(range(1,11))*10.py":##"4_0_0_[1].py":#"1_1_0_list(range(1,11))*10.py":
        #     continue
        # if file_name!="1_0_0_list(range(1,100001))_func.py":#"1_1_0_list(range(1,11))*10.py":##"4_0_0_[1].py":#"1_1_0_list(range(1,11))*10.py":
        #     continue
        # if file_name!="1_2_1_[1].py":# "4_4_4_[1].py" "2_4_1_[1].py" "1_3_3_[1].py" "1_1_4_list(range(1,11)).py" "1_0_0_[1].py" "2_3_3_[1].py" "2_4_2_[1].py" "1_0_1_[].py" "2_4_0_[1].py" "2_1_2_[1].py":#"2_4_3_[1].py":#"1_1_0_list(range(1,11))*10.py":
        #     continue

        time_start = time.time()
        print(">>>>come file: ", file_name)
        # continue
        if '.py' not in file_name:
            continue
        code_list = refactor_set_comprehension.refactor_set_comprehension(bench_dir + file_name)
        # for code in code_list:
        #     print("code: ",code)
        # break
        if len(code_list) > 1:
            print("the file has errors, please check! ", bench_dir + file_name)
            continue
        for ind, (for_node, assign_node, remove_ass_flag, new_tree) in enumerate(code_list):
            file_path = bench_dir + file_name
            # if os.path.exists(bench_time_info_dir+file_name[:-3]+".pkl"):
            #     continue
            count_remain+=1
        save_one_file_time_list(file_name, code_list,invocations,iterations)
        # break
    print("count_remain: ", count_remain)

        # break
    total_end_time = time.time()
    print("total time: ", total_end_time - total_start_time)

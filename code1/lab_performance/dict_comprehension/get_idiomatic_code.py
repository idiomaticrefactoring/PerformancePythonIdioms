import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_dict_comprehension
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


def save_one_file_time_list(file_name, code_list):
    for ind, (for_node, assign_node, remove_ass_flag, new_tree) in enumerate(code_list):
        file_path = bench_dir + file_name
        # if os.path.exists(bench_time_info_dir + file_name[:-3] + ".pkl"):
        #     continue
        # if 1:  # not os.path.exists(time_complicate_bench_dir+file_name):
        #     old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category_insert_time_complete(
        #         file_path, for_node,
        #         assign_node,
        #         new_tree, remove_ass_flag)
        #     '''
        #     print("old_content: ")
        #     print(old_content)
        #     print("new_content: ")
        #     print(new_content)
        #     '''
        #     new_add_iterations_content = lab_performance_util.insert_iterations(new_content, iterations)
        #     '''
        #     print("new_add_iterations_content: ")
        #     print(new_add_iterations_content)
        #     print(">>>>>>>>>>>>>>>>whether timing new content and old content is same: ", flag_same)
        #     '''
        #     util.save_file_path(time_complicate_bench_dir + file_name, new_add_iterations_content)
        if 1:  # not os.path.exists(time_simp_bench_dir + file_name):
            # old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category(
            #     file_path, for_node,
            #     assign_node,
            #     new_tree, remove_ass_flag)
            old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category_no_add_time(
                file_path, for_node,
                assign_node,
                new_tree, remove_ass_flag)
            print("new_content: ")
            print(new_content)
            util.save_file_path(bench_dir_no_idiomatic + file_name, new_content)


            # '''
            # new_add_iterations_content = lab_performance_util.insert_iterations(new_content, iterations)
            # util.save_file_path(time_simp_bench_dir + file_name, new_add_iterations_content)

        # lab_code_info=util.load_pkl(bench_time_info_dir, file_name[:-3])
        # print(lab_code_info)
        # print(lab_code_info.code_info)
        print("save time for file has finished! ", bench_time_info_dir + file_name)
    print("one file time: ", time.time() - time_start)
if __name__ == '__main__':
    iterations = 35#35
    invocations = 50
    thresh_invo = 50
    # iterations=20
    # invocations=30
    warms_up=3
    window=4
    pro_time_start = time.time()
    log_time_complicate_bench_dir = util.data_root_mv + "lab_performance/dict_compre_benchmarks/log/log_time_compli_code_prefined_cpu_new/"
    # log_time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/log/log_time_list_compreh_compli_code/"
    log_time_simp_bench_dir = util.data_root_mv + "lab_performance/dict_compre_benchmarks/log/log_time_simp_code_prefined_cpu_new/"
    # util.mkdirs(log_time_complicate_bench_dir)
    # util.mkdirs(log_time_simp_bench_dir)
    # time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/code/time_complicated_code/"
    time_complicate_bench_dir = util.data_root_mv + "lab_performance/dict_compre_benchmarks/code/time_complicated_code_prefined_cpu_new/"
    time_simp_bench_dir = util.data_root_mv + "lab_performance/dict_compre_benchmarks/code/time_simple_code_prefined_cpu_new/"

    # util.mkdirs(time_complicate_bench_dir)
    # util.mkdirs(time_simp_bench_dir)
    bench_time_info_dir = util.data_root_mv + "lab_performance/dict_compre_benchmarks/prefined_cpus_remain_code_new/"
    bench_dir_no_idiomatic = util.data_root + "lab_performance/dict_compre_benchmarks_no_idiomatic/code/code/"

    # util.mkdirs(bench_time_info_dir)
    bench_dir = util.data_root_mv + "lab_performance/dict_compre_benchmarks/code/code/"
    total_start_time=time.time()
    prefined_cpu = "taskset -c 6,7 "
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
    filter_file_name_list =['list(range(1,1000001))','list(range(1,1001))','list(range(1,101))','list(range(1,33))']
    # filter_file_name = "list(range(1,10000001))"#900
    # filter_file_name_list=["1_0_0_[]_func.py","1_0_0_[1]_func.py","1_0_0_list(range(1,11))_func.py","1_0_0_list(range(1,101))_func.py","1_0_0_list(range(1,1001))_func.py","1_0_0_list(range(1,10001))_func.py"]
    count_remain=0
    offset = 1066#offset
    end = None
    for file_name in dir_list[:]:

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
        code_list = refactor_dict_comprehension.refactor_dict_comprehension(bench_dir + file_name)

        # for code in code_list:
        #     print("code: ",code)

        save_one_file_time_list(file_name, code_list)
        # break
    print("count_remain: ", count_remain)

        # break
    total_end_time = time.time()
    print("total time: ", total_end_time - total_start_time)

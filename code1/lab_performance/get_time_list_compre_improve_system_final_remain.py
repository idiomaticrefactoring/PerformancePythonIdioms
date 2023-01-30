import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_list_comprehension
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
if __name__ == '__main__':
    iterations=20
    invocations=30
    warms_up=3
    window=4
    pro_time_start = time.time()
    log_time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/remain_code_1/log/log_time_list_compreh_compli_code_prefined_cpu/"
    # log_time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/log/log_time_list_compreh_compli_code/"
    log_time_simp_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/remain_code_1/log/log_time_list_compreh_simp_code_prefined_cpu/"
    util.mkdirs(log_time_complicate_bench_dir)
    util.mkdirs(log_time_simp_bench_dir)
    # time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/code/time_complicated_code/"
    time_complicate_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/remain_code_1/code/time_complicated_code_prefined_cpu/"
    time_simp_bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/remain_code_1/code/time_simple_code_prefined_cpu/"

    util.mkdirs(time_complicate_bench_dir)
    util.mkdirs(time_simp_bench_dir)
    bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/remain_code_1/prefined_cpus_remain_code/"
    util.mkdirs(bench_time_info_dir)
    bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/code/code/"#code/
    total_start_time=time.time()
    prefined_cpu = "taskset -c 2,3 "
    print("total number: ",len(os.listdir(bench_dir)))
    import random
    # dir_list=list(os.listdir(bench_dir))
    remain_dir=util.data_root + "lab_performance/list_compre_benchmarks/prefined_cpus_remain_code_2/"

    # remain_dir=util.data_root + "lab_performance/list_compre_benchmarks/prefined_cpus_remain_code_1/"
    dir_list = util.load_json(remain_dir, "prefined_cpus_remain_unstable")
    random.seed(2022)
    random.shuffle(dir_list)
    # print(dir_list)

    for file_name in dir_list[:16]:

        # if file_name=="2_3_0_list(range(1,11))*1000.py":
        #     continue
        # if file_name!="2_4_3_[1].py":#"1_1_0_list(range(1,11))*10.py":##"4_0_0_[1].py":#"1_1_0_list(range(1,11))*10.py":
        #     continue
        # if file_name!="1_2_1_[1].py":# "4_4_4_[1].py" "2_4_1_[1].py" "1_3_3_[1].py" "1_1_4_list(range(1,11)).py" "1_0_0_[1].py" "2_3_3_[1].py" "2_4_2_[1].py" "1_0_1_[].py" "2_4_0_[1].py" "2_1_2_[1].py":#"2_4_3_[1].py":#"1_1_0_list(range(1,11))*10.py":
        #     continue

        time_start = time.time()
        print(">>>>come file: ", file_name)
        # continue
        if '.py' not in file_name:
            continue
        code_list = refactor_list_comprehension.refactor_list_comprehension(bench_dir + file_name)
        # for code in code_list:
        #     print("code: ",code)
        if len(code_list) > 1:
            print("the file has errors, please check! ", bench_dir + file_name)
            continue
        for ind, (for_node, assign_node, remove_ass_flag, new_tree) in enumerate(code_list):
            file_path = bench_dir + file_name
            if 1:  # not os.path.exists(time_complicate_bench_dir+file_name):
                old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category_insert_time_complete(
                    file_path, for_node,
                    assign_node,
                    new_tree, remove_ass_flag)
                '''
                print("new_content: ")
                print(new_content)
                '''
                new_add_iterations_content = lab_performance_util.insert_iterations(new_content, iterations)
                '''
                print("new_add_iterations_content: ")
                print(new_add_iterations_content)
                print(">>>>>>>>>>>>>>>>whether timing new content and old content is same: ", flag_same)
                '''
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
                util.save_file_path(time_simp_bench_dir + file_name, new_add_iterations_content)
            all_time_list = []
            all_pythonic_time_list = []
            num_add_ele = None
            stable_invo=0
            for invo in range(invocations):
                output = lab_performance_util.sequence_run(time_complicate_bench_dir, file_name, invo=invo,
                                                           log_dir=log_time_complicate_bench_dir + file_name[:-3] + "/",
                                                           prefined_cpu=prefined_cpu)
                get_time_list = lab_performance_util.get_time_list(output)
                time_list = [float(e) for e in get_time_list[warms_up:]]
                stable_flag=lab_performance_util.whether_cov(time_list, window)
                stable_invo+=stable_flag

                all_time_list.append(get_time_list)
                if invo == 0:
                    # print(get_time_list)
                    num_add_ele = lab_performance_util.get_num_add_ele(output)
                if stable_invo >= 10:
                    print(file_name, " complicated code is stable when invocations are : ", invo + 1)
                    break

                    # print("num_add_ele: ",num_add_ele)
            stable_invo_idiom = 0
            for invo in range(invocations):
                output = lab_performance_util.sequence_run(time_simp_bench_dir, file_name, invo=invo,
                                                           log_dir=log_time_simp_bench_dir + file_name[:-3] + "/",
                                                           prefined_cpu=prefined_cpu
                                                           )
                get_pythonic_time_list = lab_performance_util.get_pythonic_time_list(output)
                time_list = [float(e) for e in get_pythonic_time_list[warms_up:]]
                stable_flag = lab_performance_util.whether_cov(time_list, window)
                stable_invo_idiom += stable_flag
                all_pythonic_time_list.append(get_pythonic_time_list)
                if stable_invo_idiom>=10:
                    print(file_name," simple code is stable when invocations are : ", invo + 1)
                    break
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
            # '''
            # lab_code_info=util.load_pkl(bench_time_info_dir, file_name[:-3])
            # print(lab_code_info)
            # print(lab_code_info.code_info)
            print("save time for file has finished! ", bench_time_info_dir + file_name)
        print("one file time: ", time.time() - time_start)
        # break
    total_end_time = time.time()
    print("total time: ", total_end_time - total_start_time)
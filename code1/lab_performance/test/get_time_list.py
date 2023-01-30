import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
print("code_dir: ",code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"wrap_refactoring/")
import lab_performance_util
import util
from lab_code_info import LabCodeInfo
if __name__ == '__main__':
    invocations=1
    all_time_list = []
    all_pythonic_time_list = []
    time_complicate_bench_dir="./"
    time_simp_bench_dir="./"
    log_time_complicate_bench_dir="log/log_time_complicate/"
    log_time_simp_bench_dir="log/log_time_simp/"
    bench_time_info_dir="time/"#"time_own/"
    prefined_cpu = "taskset -c 2,3 "
    dict_time_file_name="time_for_2"
    dict_time_file_name="time_for_1_slow_reason"
    dict_time_file_name = "time_for_1_slow_reason_add_gc"
    # dict_time_file_name="time_for_1_timeit"

    #'''
    for invo in range(invocations):
        file_name="list_comprehension_complicated_timeit_slow_reason.py"#"list_comprehension_complicated.py"#"list_comprehension_complicated_own_insert_2_for.py"#"list_comprehension_complicated_own_insert.py"#"list_comprehension_complicated.py"
        output = lab_performance_util.sequence_run_norm(time_complicate_bench_dir, file_name, invo=invo,
                                                   log_dir=log_time_complicate_bench_dir + file_name[:-3] + "/",
                                                   prefined_cpu=prefined_cpu)
        get_time_list = lab_performance_util.get_time_list(output)
        time_list = [float(e) for e in get_time_list]

        all_time_list.append(time_list)
        print("time_list: ",time_list)
    for invo in range(invocations):
        file_name ="list_comprehension_timeit_slow_reason.py"#"list_comprehension.py"#"list_comprehension_own_insert_2_for.py" #"list_comprehension_own_insert.py"#"list_comprehension.py"
        output = lab_performance_util.sequence_run_norm(time_simp_bench_dir, file_name, invo=invo,
                                                   log_dir=log_time_simp_bench_dir + file_name[:-3] + "/",
                                                   prefined_cpu=prefined_cpu
                                                   )
        get_pythonic_time_list = lab_performance_util.get_pythonic_time_list(output)
        time_list = [float(e) for e in get_pythonic_time_list]
        all_pythonic_time_list.append(time_list)
        print("get_pythonic_time_list: ", get_pythonic_time_list)
    dict_time_list={"all_time_list":all_time_list,
                    "all_pythonic_time_list":all_pythonic_time_list}
    util.save_pkl(bench_time_info_dir, dict_time_file_name, dict_time_list)
    #'''
    # file_name="list_comprehension_own_insert"#"list_comprehension"dict_time_file_name#"list_comprehension_own_insert"--这个是一个for
    # bench_time_info_dir=#"time/"
    dict_time_list = util.load_pkl(bench_time_info_dir, dict_time_file_name)
    print(dict_time_list)
    all_time_list=dict_time_list['all_time_list']
    all_pythonic_time_list=dict_time_list['all_pythonic_time_list']
    time=sum([sum(e) for e in all_time_list])
    time_pythonic = sum([sum(e) for e in all_pythonic_time_list])
    print(time/time_pythonic,time_pythonic/time)
    # print(sum(all_time_list),sum(all_pythonic_time_list))


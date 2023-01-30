import sys, ast, os, csv, time, traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + "performance/")
# sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir + "test_case/")
import util, get_test_case_acc_util, performance_util, configure_pro_envir_util
import code_info
from code_info import CodeInfo
from extract_simp_cmpl_data import ast_util
import ast_performance_util
# import replace_content_by_ast_time_percounter
import performance_replace_content_by_ast_multi_assign
if __name__ == '__main__':

    pro_time_start = time.time()
    save_code_info_dir=util.data_root+"performance/a_multi_assign/a_multi_assign_iter_invoca/"
    error_code_dir = util.data_root + "performance/a_multi_assign/erro_record_dir/"
    time_out_dir=util.data_root + "performance/a_multi_assign/time_out_record_dir/"
    file_dir=util.data_root+"format_code_info/"
    file_name="multi_ass_sample_317"#"multi_ass_complete"
    code_time_list=[]
    case_is_true_list_filter = []
    time_out_list_filter=[]
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    # invocations = 2
    print("total number of multiple ass: ",len(os.listdir(save_code_info_dir)))
    case_is_true_list_filter=util.load_pkl(error_code_dir, "error_code_is_true_info")
    time_out_list_filter=util.load_pkl(time_out_dir, "time_out_code_info")
    case_is_true_list_filter += util.load_pkl(error_code_dir, "error_code_is_true_info_2")
    time_out_list_filter += util.load_pkl(time_out_dir, "time_out_code_info_2")
    case_is_true_list_filter += util.load_pkl(error_code_dir, "error_code_is_true_info_3")
    time_out_list_filter += util.load_pkl(time_out_dir, "time_out_code_info_3")
    case_is_true_list_filter=util.load_pkl(error_code_dir, "error_code_is_true_info_update_some" )
    time_out_list_filter=util.load_pkl(time_out_dir, "time_out_code_info_update_some")
    print("case_is_true: ",len(case_is_true_list_filter))
    print("time_out_list_filter: ", len(time_out_list_filter))
    save_code_info_dir_add_performance_change=util.data_root_mv + "performance/a_multi_assign/a_multi_assign_iter_invoca_add_perf_change_new/"
    file_name_list=[]
    for e in os.listdir(save_code_info_dir_add_performance_change):
        file_name_list.append(e)
        # print(e)
        # break

    total_file_name_list=[]
    for e in os.listdir(save_code_info_dir):
        total_file_name_list.append(e)
        # print(e)
        # break
    print(len(total_file_name_list),len(file_name_list),set(total_file_name_list)-set(file_name_list))
    #{'geojson.utils.generate_random_246.pkl', 'gym.envs.toy_text.frozen_lake.generate_random_map_264.pkl'}
    #{904M,9.8G}

    bench_time_info_dir=util.data_root+"performance/a_multi_assign/a_multi_assign_iter_invoca/"

    # bench_time_info_dir=util.data_root+"performance/a_multi_assign/a_multi_assign_iter_invoca_update_some/"

    csv_perf_change_dir = util.data_root + "performance/a_multi_assign/csv/"
    file_name_list = []

    for ind, file_name in enumerate(sorted(os.listdir(bench_time_info_dir)[:])):
        # print("file_name: ",file_name[:-4].split("_")[-1])
        # break
        if file_name.endswith('.log'):
            continue
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: CodeInfo
        file_html = lab_code_info.file_html
        if file_html!="https://github.com/borgmatic-collective/borgmatic/tree/master/borgmatic/config/generate.py":
            continue
        print(">>>>>>>>>pythonic time: ")
        print(lab_code_info.compli_code_time_dict[:2])
        print(">>>>>>>>>complicated time: ")
        print(lab_code_info.simple_code_time_dict[:2])

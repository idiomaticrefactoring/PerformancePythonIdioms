
import sys, ast, os, csv, time, traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + "performance/")
# sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir + "test_case/")
import util, get_test_case_acc_util, performance_util, configure_pro_envir_util
import code_info
from extract_simp_cmpl_data import ast_util
import ast_performance_util
# import replace_content_by_ast_time_percounter
import performance_replace_content_by_ast_multi_assign
if __name__ == '__main__':
    file_dir=util.data_root+"format_code_info/"
    file_name="multi_ass_swap"#"multi_ass_complete"
    # util.save_pkl(util.data_root + "format_code_info/", "multi_ass_swap", list_code_info_list)
    file_name_no_swap="multi_ass_sample_317"#"multi_ass_complete"

    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    swap_code_info_list = util.load_pkl(file_dir, file_name_no_swap)
    total_code_info_list=code_info_list+swap_code_info_list
    file_name_swap_and_noswap="multi_ass_swap_and_noswap"#"multi_ass_complete"
    util.save_pkl(file_dir, file_name_swap_and_noswap, total_code_info_list)


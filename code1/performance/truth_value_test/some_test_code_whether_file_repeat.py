import sys,ast,os,csv,time,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
# sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"test_case/")
import util,get_test_case_acc_util,performance_util,configure_pro_envir_util
import code_info
from extract_simp_cmpl_data import ast_util
import ast_performance_util
# import replace_content_by_ast_time_percounter
import performance_replace_content_by_ast_time_percounter

if __name__ == '__main__':

    pro_time_start = time.time()
    # save_code_info_dir=util.data_root+"performance/list_compre_benchmarks_new_test_single_file_2/"
    # save_code_info_dir=util.data_root+"performance/list_compre_benchmarks_new_test_single_file_3/"
    # save_code_info_dir=util.data_root+"performance/list_compre_benchmarks_iter_improv_final/"

    file_dir=util.data_root+"format_code_info/"
    file_name = "truth_value_test_complete"#"multi_ass_sample_317_20"#"multi_ass_sample_317_2021"#"multi_ass_sample_317"
    # file_name="list_compre"
    code_time_list=[]
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    invocations = 50
    threshold = 50
    iterations = 35
    # invocations = 2#50
    # threshold = 1#10
    # iterations = 2#15
    prefine_cpus="taskset -c 2,3 "
    offset = 0#44#88
    print("total number of code: ",len(code_info_list))
    file_html_1,file_html_2,file_html_3=[],[],[]
    for ind_code,code in enumerate(code_info_list[:213]):
        # if ind_code>0:
        #     break
        code:code_info.CodeInfo
        file_html=code.file_html
        if file_html=='https://github.com/nipy/nibabel/tree/master/nibabel/fileslice.py':
            print(ind_code,file_html)
        file_html_1.append(file_html)
    for ind_code,code in enumerate(code_info_list[213:427]):
        # if ind_code>0:
        #     break
        code:code_info.CodeInfo
        file_html=code.file_html
        if file_html=='https://github.com/nipy/nibabel/tree/master/nibabel/fileslice.py':
            print(ind_code,file_html)
        if file_html=='https://github.com/airspeed-velocity/asv/tree/master/asv/commands/compare.py':
            print(ind_code,file_html)
        file_html_2.append(file_html)
    for ind_code,code in enumerate(code_info_list[427:]):
        # if ind_code>0:
        #     break
        code:code_info.CodeInfo
        file_html=code.file_html
        if file_html=='https://github.com/airspeed-velocity/asv/tree/master/asv/commands/compare.py':
            print(ind_code,file_html)
        file_html_3.append(file_html)
    print("intersect: ",len(set(file_html_1)&set(file_html_2)),len(set(file_html_2)&set(file_html_3)),len(set(file_html_1)&set(file_html_3)))
    file_name = "truth_value_test_sample_remain_all"  # "multi_ass_sample_317_20"#"multi_ass_sample_317_2021"#"multi_ass_sample_317"
    # file_name="list_compre"
    code_time_list = []
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    file_html_4=[]
    for ind_code,code in enumerate(code_info_list[:120]):
        # if ind_code>0:
        #     break
        code:code_info.CodeInfo
        file_html=code.file_html
        file_html_4.append(file_html)
    file_html_5 = []
    for ind_code,code in enumerate(code_info_list[120:240]):
        # if ind_code>0:
        #     break
        code:code_info.CodeInfo
        file_html=code.file_html
        file_html_5.append(file_html)
    file_html_6 = []
    for ind_code, code in enumerate(code_info_list[240:]):
        # if ind_code>0:
        #     break
        code: code_info.CodeInfo
        file_html = code.file_html
        file_html_6.append(file_html)
    print("intersect: ",len(set(file_html_1)&set(file_html_4)),len(set(file_html_2)&set(file_html_4)),
          len(set(file_html_3)&set(file_html_4)))
    print("intersect: ",len(set(file_html_1)&set(file_html_5)),len(set(file_html_2) & set(file_html_5)),
          len(set(file_html_3) & set(file_html_5)))
    print("intersect: ", len(set(file_html_6) & set(file_html_5)))

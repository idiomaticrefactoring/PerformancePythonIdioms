import sys,ast,os,csv,time,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-4])+"/"

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
    file_dir=util.data_root+"format_code_info/"
    file_name="list_compre"
    code_time_list=[]
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    invocations = 30
    threshold = 10
    iterations = 15
    prefine_cpus = "taskset -c 2,3 "
    offset = 0
    end = 44
    for_num_list=[1,10,100,1000,10000,100000]#[1]#
    # for for_num in for_num_list:
    file_name_list=[]
    file_name_list_1=[]
    file_name_list_2 = []
    if 1:
        pass
        # for_num=2
        for ind_code, code in enumerate(code_info_list[offset:44]):
            # if ind_code>0:
            #     break
            code:code_info.CodeInfo
            file_html=code.file_html
            file_name_list.append(file_html)

        for ind_code, code in enumerate(code_info_list[44:88]):
            # if ind_code>0:
            #     break
            code:code_info.CodeInfo
            file_html=code.file_html
            file_name_list_1.append(file_html)

        for ind_code, code in enumerate(code_info_list[88:]):
            # if ind_code>0:
            #     break
            code:code_info.CodeInfo
            file_html=code.file_html
            file_name_list_2.append(file_html)
    print("intersect: ",set(file_name_list)&set(file_name_list_1),
          set(file_name_list)&set(file_name_list_2),
          set(file_name_list_1) & set(file_name_list_2) )

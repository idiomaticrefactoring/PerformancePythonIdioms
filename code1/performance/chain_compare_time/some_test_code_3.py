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

    file_path="some_test_code_2.py"
    # def replace_content_chain_compar_insert_time(file_path, compl_node, sim_node, me_name):
    content = util.load_file_path(file_path)
    all_tree = ast.parse(content)
    me_name="single_var"
    ana_py = ast_performance_util.Fun_Analyzer_Insert_Stmt(me_name)
    ana_py.visit(all_tree)
    print("come here: ",ast.unparse(all_tree))
        # return content, ast.unparse(all_tree), old_tree_str == ast.unparse(all_tree)

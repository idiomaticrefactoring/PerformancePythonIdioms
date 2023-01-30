import os,sys
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
import util,copy

from extract_simp_cmpl_data import ast_util
from extract_transform_complicate_code_new.extract_compli_var_unpack_star_call_improve import get_func_call_by_args

# from code1.extract_simp_cmpl_data import ast_util
from transform_c_s import transform_var_unpack_call_compli_to_simple
from tokenize import tokenize
import ast,traceback
def refactor_call_star(file_path,end_str=0):
    try:
        flag_end=int(file_path.split("/")[-1].split("_")[0])
    except:
        flag_end =0
    content = util.load_file_path(file_path)
    # print("content:\n",content)
#     content='''
# def f():
#     for configdir in configdirs:
#         for configext in configexts:
#             locations.append(os.path.join(configdir[0]))
# '''
    new_code_list=[]
    try:
        file_tree = ast.parse(content)
        ana_py = ast_util.Fun_Analyzer()
        ana_py.visit(file_tree)
        # print("ana_py.func_def_list ", ana_py.func_def_list)
        # dict_file["repo_name"]=repo_name
        for tree, class_name in ana_py.func_def_list:

            new_arg_same_list = get_func_call_by_args(tree)

            for ind, arg_info_list in enumerate(new_arg_same_list):
                copy_arg_info_list = copy.deepcopy(arg_info_list)
                star_node = transform_var_unpack_call_compli_to_simple.transform_var_unpack_call_each_args(
                    copy_arg_info_list)
                # print("new code: ",ast.unparse(star_node))
                upper = star_node.value.value.slice.upper
                upper_value = ast.unparse(upper)
                lower = star_node.value.value.slice.lower
                lower_value = ast.unparse(lower)
                step = star_node.value.value.slice.step
                step_value = ast.unparse(step)
                if end_str and lower_value == '0' and step_value == '1':
                    star_node.value.value=star_node.value.value.value
                else:
                    if end_str:
                        star_node.value.value.slice.upper = None

                    if lower_value == '0':
                        star_node.value.value.slice.lower = None

                    if step_value == '1':
                        star_node.value.value.slice.step = None
                # print("new code: ", ast.unparse(star_node))

                new_code_list.append([arg_info_list, star_node])


    except:
        traceback.print_exc()
    return new_code_list
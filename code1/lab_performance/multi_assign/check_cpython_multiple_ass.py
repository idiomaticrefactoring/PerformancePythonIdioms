import sys, ast, os, csv, time, copy

import subprocess
from pathos.multiprocessing import ProcessingPool as newPool

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir+"extract_idiom_code_new/")
sys.path.append(code_dir+"lab_performance/")
import pandas as pd
from extract_simp_cmpl_data import ast_util
import util,lab_performance_util
from lab_code_info import LabCodeInfo
from extrac_idiom_assign_multiple import get_idiom_assign_multi

# save_repo_for_else_complicated(repo_name)
def save_repo_for_else_complicated(repo_name):
    count_complicated_code=0
    #print("come the repo: ", repo_name)
    one_repo_for_else_code_list = []
    dict_file = dict()
    for file_info in os.listdir(cpython_dir+repo_name):
        if not file_info.endswith(".py"):
            continue
        file_path=file_info
        file_path = file_info["file_path"]
        # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
        #     continue
        file_html = file_info["file_html"]
        #print("come this file: ", file_path)
        try:
            content = util.load_file_path(file_path)
        except:
            print(f"{file_path} is not existed!")
            continue
        #print("content: ",content)
        try:
            file_tree = ast.parse(content)
            ana_py = ast_util.Fun_Analyzer()
            ana_py.visit(file_tree)

            dict_class = dict()
            for tree, class_name in ana_py.func_def_list:
                code_list=get_idiom_assign_multi(tree)
                if code_list:
                    ast_util.set_dict_class_code_list(tree, dict_class, class_name, code_list)

            #print("func number: ",file_html,len(ana_py.func_def_list))
            # for tree in ana_py.func_def_list:
            #     #print("tree_ func_name",tree.__dict__)
            #     code_list.extend(get_idiom_assign_multi(tree))
            # if code_list:
            #         one_repo_for_else_code_list.append([code_list, file_path, file_html])
            if dict_class:
                dict_file[file_html] = dict_class
        except SyntaxError:
            print("the file has syntax error")
            continue
        except ValueError:

            traceback.print_exc()

            print("the file has value error: ", file_html)

            continue
        #break
if __name__ == '__main__':
    cpython_dir = util.data_root + "python_star_2000repo/"
    repo_name = "cpython-main"
    dict_file=dict()
    for ind,(path,dir_list,file_list) in enumerate(os.walk(cpython_dir+repo_name)):
        for file in file_list:
            # print(path+file)

            file_path=path+"/"+file
            if not file_path.endswith('.py'):
                continue
            try:
                content = util.load_file_path(file_path)
            except:
                print(f"{file_path} is not existed!")
                continue
            # print("content: ",content)
            try:
                file_tree = ast.parse(content)
                ana_py = ast_util.Fun_Analyzer()
                ana_py.visit(file_tree)

                dict_class = dict()
                for tree, class_name in ana_py.func_def_list:
                    code_list = get_idiom_assign_multi(tree)
                    if code_list:
                        ast_util.set_dict_class_code_list(tree, dict_class, class_name, code_list)

                # print("func number: ",file_html,len(ana_py.func_def_list))
                # for tree in ana_py.func_def_list:
                #     #print("tree_ func_name",tree.__dict__)
                #     code_list.extend(get_idiom_assign_multi(tree))
                # if code_list:
                #         one_repo_for_else_code_list.append([code_list, file_path, file_html])

                if dict_class:
                    print(">>>>>>>>>dict_class: ", file_path,dict_class)
                    dict_file[file_path] = dict_class
            except SyntaxError:
                print("the file has syntax error")
                continue
            except ValueError:

                traceback.print_exc()

                print("the file has value error: ", file_path)

                continue
        # if not file_info.endswith(".py"):
        #     continue
        # print(file_info)
        # break
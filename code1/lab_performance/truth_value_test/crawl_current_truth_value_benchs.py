import sys,ast,os,csv,time,copy,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"extract_idiom_code_new/")
sys.path.append(code_dir+"wrap_refactoring/")
# transform_complicate_to_simple_pkl_improve_new_modify_bugs_final

from extrac_idiom_truth_value_test_remove_is_improve import get_idiom_truth_value_test_add_node

import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util
from lab_code_info import LabCodeInfo
import time
import pandas as pd
import numpy as np, scipy.stats as st

from pathos.multiprocessing import ProcessingPool as newPool
from extract_simp_cmpl_data import ast_util
import subprocess


if __name__ == '__main__':
    # '''
    # save_complicated_code_dir_pkl= util.data_root + "lab_performance/test_case_benchmarks/chained_comparison_idiom_code/"
    dict_repo_file_python= util.load_json(util.data_root, "python3_1000repos_files_info")
    csv_chain_compare_idiom=util.data_root + "lab_performance/csv/csv_truth_value_test_idiom.csv"
    # repo_list = []
    # for ind, repo_name in enumerate(dict_repo_file_python):
    #     repo_list.append(repo_name)
    #     # if ind>5:
    #     #     break
    #     # break
    # print("count: ", len(repo_list))
    # repo_list=["cpython-main"]
    # pool = newPool(nodes=30)
    # pool.map(save_repo_for_else_complicated, repo_list)  # [:3]sample_repo_url ,token_num_list[:1]
    # pool.close()
    # pool.join()
    cpython_dir = util.data_root + "python_star_2000repo/"
    repo_name = "cpython-main"
    dict_file = dict()
    for ind, (path, dir_list, file_list) in enumerate(os.walk(cpython_dir + repo_name)):
        for file in file_list:
            # print(path+file)

            file_path = path + "/" + file
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
                    code_list = get_idiom_truth_value_test_add_node(tree)
                    if code_list:
                        ast_util.set_dict_class_code_list(tree, dict_class, class_name, code_list)

                # print("func number: ",file_html,len(ana_py.func_def_list))
                # for tree in ana_py.func_def_list:
                #     #print("tree_ func_name",tree.__dict__)
                #     code_list.extend(get_idiom_assign_multi(tree))
                # if code_list:
                #         one_repo_for_else_code_list.append([code_list, file_path, file_html])

                if dict_class:
                    print(">>>>>>>>>dict_class: ", file_path, dict_class)
                    dict_file[file_path] = dict_class
            except SyntaxError:
                print("the file has syntax error")
                continue
            except ValueError:

                traceback.print_exc()

                print("the file has value error: ", file_path)

                continue
            # break
        # '''
        # break
    dict_pd = {
        "repo_name": [], "file_html": [], "class_name": [], "me_name": [], "code_str": []
    }
    complicate_code = dict_file
    for file_html in complicate_code:
        dict_class = complicate_code[file_html]
        for class_name in dict_class:
            for me_id in dict_class[class_name]:
                new_code_list = dict_class[class_name][me_id]
                for code_str,node,other in new_code_list:
                    dict_pd["repo_name"].append(repo_name)
                    dict_pd["file_html"].append(file_html)
                    dict_pd["class_name"].append(class_name)
                    dict_pd["me_name"].append(me_id)
                    dict_pd["code_str"].append(code_str+"/n"+node)
    dataMain = pd.DataFrame(data=dict_pd)
    # print(">>>>>>drop same features: ", dataMain.keys())
    # print(dataMain.to_dict())
    dataMain.to_csv(csv_chain_compare_idiom, index=False)
    # save_code_test()
        # '''

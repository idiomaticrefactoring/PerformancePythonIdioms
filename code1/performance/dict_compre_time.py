import sys, ast, os, csv, time, traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + "test_case/")
import util, get_test_case_acc_util, performance_util, configure_pro_envir_util
import code_info
from extract_simp_cmpl_data import ast_util
import ast_performance_util
import replace_content_by_ast_time_percounter




if __name__ == '__main__':
    pro_time_start = time.time()
    file_dir = util.data_root + "format_code_info/"
    file_name = "set_compre"#"dict_compre"
    code_time_list = []
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    for ind_code, code in enumerate(code_info_list):
        # if code.own_config==0:
        #     continue
        # if ind_code>0:
        #     break
        code: code_info.CodeInfo
        file_html = code.file_html
        test_me_inf_list = code.test_case_info_list
        for_node, assign_node, remove_ass_flag, new_tree = code.code_info
        cl, me, repo_name = code.cl, code.me, code.repo_name
        me_name = me.split("$")[0]
        if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
            continue
        total_name = get_test_case_acc_util.get_total_name(file_html, cl, me_name)
        repo_path = pro_path + repo_name + "/"
        real_file_html = file_html.replace("//", "/")
        rela_path = real_file_html.split("/")[6:]
        old_path = repo_path + "/".join(rela_path)
        performance_util.backup_content(repo_path, file_html)

        print(">>>>>>>>>>>>>>>>come total_name: ", file_html, cl, me_name, total_name)
        '''
        real_file_html = file_html.replace("//", "/")
        rela_path = real_file_html.split("/")[6:]
        old_path = repo_path + "/".join(rela_path)
        print("for_node: ", for_node.lineno)  # ,new_content_insert_time)
        rela_path_test_file_name = "".join(
            [rela_path[-1][:-3], util.copy_file_suffix+"_test_insert_timeit", ".py"])
        rela_path_test_pythonic_file_name = "".join(
            [rela_path[-1][:-3], util.copy_file_suffix+"_test_insert_timeit_pythonic", ".py"])
        rela_path[-1] = "".join([rela_path[-1][:-3], util.copy_file_suffix, ".py"])
        rela_path_test = "/".join(rela_path[:-1]) + "/" + rela_path_test_file_name
        rela_path_test_pythonic = "/".join(rela_path[:-1]) + "/" + rela_path_test_pythonic_file_name
        # util.save_file_path(repo_path + rela_path_test, new_content_insert_time)

        # get_index(old_content.split("\n"), ast.unparse(old_tree)[])
        # print("test old content: ",len(old_content.split("\n")),old_content.split("\n")[old_tree.lineno])
        # print("test new content: ", len(new_content.split("\n")),new_content[new_tree.lineno])
        # print(">>>>>>>>>>old_tree: ",init_ass_remove_flag,old_tree.lineno,new_tree.lineno, ast.unparse(old_tree),ast.unparse(new_tree))
        rela_path = "/".join(rela_path)
        print("copy_file_path: ",repo_path+rela_path)
        old_content = util.load_file_path(old_path)
        util.save_file_path(repo_path + rela_path, old_content)  # copy 一份原来的文件防止失去
        '''

        # flag_suc = performance_util.code_test(repo_path, old_path, old_content, test_me_inf_list)
        # flag_suc=1
        # '''
        # all_repeat_old_time = []
        # all_repeat_new_time = []
        # all_repeat_new_var = []

        for i in range(1):

            # '''
            old_content, new_content, flag_same = replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category_insert_time(
                repo_name, file_html, for_node,
                assign_node,
                new_tree, remove_ass_flag)
            print(">>>>>>>>>>>>>>>>whether timing new content and old content is same: ", flag_same)
            print(new_content)
            #'''
            util.save_file_path(old_path, new_content)

            # performance_util.backup_time_content(repo_path,file_html,new_content)
            # util.save_file_path(repo_path + rela_path_test_pythonic,
            #                     new_content)
            print("is self config: ",code.own_config)
            all_test_case_time_list_old = performance_util.code_test_get_time(repo_path, old_path,
                                                             old_content,
                                                             test_me_inf_list,0,code.own_config,1)
            #'''
            old_content, new_content, flag_same = replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category(
                repo_name, file_html, for_node,
                assign_node,
                new_tree, remove_ass_flag)
            print(">>>>>>>>>>>>>>>>whether pythonic new content and old content is same: ", flag_same)
            # print(new_content)

            util.save_file_path(old_path, new_content)
            # performance_util.backup_pythonic_content(repo_path,file_html,new_content)
            # util.save_file_path(repo_path + rela_path_test_pythonic,
            #                     new_content)
            all_test_case_time_list_new = performance_util.code_test_get_time(repo_path, old_path,
                                                             old_content,
                                                             test_me_inf_list, 1,code.own_config,1)

            if len(all_test_case_time_list_new) != len(all_test_case_time_list_old):
                print("This test case should be discarded!", file_html, cl, me_name,len(all_test_case_time_list_new),len(all_test_case_time_list_old))
                break

            print("<<<<<<<<<<<<<<<<<<<<one code end: ", cl, me_name, total_name)
            print("all_test_case_time_list_new: \n", all_test_case_time_list_new)
            print("all_test_case_time_list_old: \n", all_test_case_time_list_old)

            code.compli_code_time_dict = all_test_case_time_list_old
            code.simple_code_time_dict = all_test_case_time_list_new
            code_time_list.append(code)
            #'''

        break
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # util.save_pkl(util.data_root + "iterations_code_time_info/"+file_name+"/", str(current_time), code_time_list)
    pro_time_end = time.time()
    print(time.time())
    print("total running time of the program: ", pro_time_end - pro_time_start)

    pass

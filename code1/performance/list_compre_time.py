import sys,ast,os,csv,time,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"test_case/")
import util,get_test_case_acc_util,performance_util,configure_pro_envir_util
import code_info
from extract_simp_cmpl_data import ast_util
import ast_performance_util
import replace_content_by_ast_time_percounter


def make_new_test_file(repo_path, test_html, cl, me,iterations=10):
    relative_test_file = "/".join(test_html.replace("//", "/").split("/")[6:])
    test_full_file_path = repo_path + relative_test_file
    copy_test_full_file_path = "".join([test_full_file_path[:-3], util.copy_file_suffix, ".py"])
    new_test_html = "".join([test_html[:-3], util.copy_file_suffix, ".py"])
    print("test_html: ", copy_test_full_file_path, test_html, new_test_html, cl, me,
          test_full_file_path)

    old_content = util.load_file_path(test_full_file_path)
    # test_code=util.load_file_path(copy_test_full_file_path)
    # print("test_code: ",test_code)
    file_tree = ast.parse(old_content)
    ana_py = ast_performance_util.Fun_Analyzer(me,iterations)
    file_tree = ana_py.visit(file_tree)
    new_test_code = ast.unparse(file_tree)
    # print("test code of test method: ", file_tree, ana_py.flag)
    # print(ast.unparse(file_tree))
    util.save_file_path(copy_test_full_file_path, new_test_code)  # copy 一份原来的文件防止失去
    copy_test_full_file_path = "".join([test_full_file_path[:-3], util.copy_file_suffix, ".py"])
    new_test_html = "".join([test_html[:-3], util.copy_file_suffix, ".py"])
    # print("test_html: ", copy_test_full_file_path, test_html, new_test_html, cl, me,
    #       test_full_file_path)
    return new_test_html
def code_test_get_time(repo_path,old_path,old_content,test_me_inf_list,is_pythonic_timeflag=0,is_own_config=0):

    all_test_case_time_list=dict()
    try:
        for test_html, each_rela_path, cl, me in test_me_inf_list:

            fun_list = ["::".join([cl, me]) if cl else me]
            new_test_html=make_new_test_file(repo_path,test_html,cl,me)
            if not is_own_config:
                run_test_result_new = configure_pro_envir_util.run_test_file_capture_output(new_test_html, repo_path, fun_list = fun_list,
                export_python = True)
            else:
                run_test_result_new = configure_pro_envir_util.run_test_file_capture_output(test_html, repo_path,
                                                                                            ven_name="venv_zejun_config",
                                                                                            fun_list=fun_list,
                                                                                            export_python=False)
            print(">>>>>>>>>>run_test_result_new: ", run_test_result_new)
            if is_pythonic_timeflag:
                get_time_list=performance_util.get_pythonic_time_list(run_test_result_new)
            else:
                get_time_list=performance_util.get_time_list(run_test_result_new)
            all_test_case_time_list[(test_html, each_rela_path, cl, me)]=get_time_list
            # print(">>>>>>>>>>run_test_result_new: ", run_test_result_new)
            # print("time_list: ", get_time_list)
            '''
            if get_time_list:
                all_test_case_time_list[(test_html, each_rela_path, cl, me)]=get_time_list            
            '''


        else:
            flag_success = 1
            #'''
            util.save_file_path(old_path, old_content)

            print("****************we save the old content to original file: ", old_path)
            #'''
    except:
        #'''
        print("****************CODE RUN OCCUR ERRORS")
        util.save_file_path(old_path, old_content)
        print("****************we save the old content to original file: ", old_path)
        
        #'''
        traceback.print_exc()
    # print(f"{loop_num} loops, total time: {end-start}")
    return all_test_case_time_list


if __name__ == '__main__':
    pro_time_start = time.time()
    file_dir=util.data_root+"format_code_info/"
    file_name="list_compre"
    code_time_list=[]
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    for ind_code,code in enumerate(code_info_list):
        # if ind_code>0:
        #     break
        code:code_info.CodeInfo
        file_html=code.file_html
        test_me_inf_list = code.test_case_info_list
        for_node, assign_node, remove_ass_flag, new_tree=code.code_info
        cl,me,repo_name=code.cl,code.me,code.repo_name
        # code.own_config=0
        # print("is ownconfig: ",code.own_config)
        # break
        me_name = me.split("$")[0]
        if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
            continue
        total_name = get_test_case_acc_util.get_total_name(file_html, cl, me_name)
        repo_path = pro_path + repo_name + "/"
        real_file_html = file_html.replace("//", "/")
        rela_path = real_file_html.split("/")[6:]
        old_path = repo_path + "/".join(rela_path)
        performance_util.backup_content(repo_path, file_html)

        print(">>>>>>>>>>>>>>>>come total_name: ", file_html,cl, me_name, total_name)

        for i in range(1):

            #'''
            old_content, new_content, flag_same = replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category_insert_time(
                repo_name, file_html, for_node,
                assign_node,
                new_tree, remove_ass_flag)
            print(">>>>>>>>>>>>>>>>whether timing new content and old content is same: ",flag_same)
            # print(new_content)
            
            util.save_file_path(old_path, new_content)

            # performance_util.backup_time_content(repo_path,file_html,new_content)
            # util.save_file_path(repo_path + rela_path_test_pythonic,
            #                     new_content)
            

            all_test_case_time_list_old = code_test_get_time(repo_path, old_path,
                                                             old_content,
                                                             test_me_inf_list)
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
            all_test_case_time_list_new = code_test_get_time(repo_path, old_path,
                                                             old_content,
                                                             test_me_inf_list,1)

            if len(all_test_case_time_list_new) != len(all_test_case_time_list_old):
                print("This test case should be discarded!",file_html,cl, me_name)
                break


            print("<<<<<<<<<<<<<<<<<<<<one code end: ", cl, me_name, total_name)
            print("all_test_case_time_list_new: \n",all_test_case_time_list_new)
            print("all_test_case_time_list_old: \n",all_test_case_time_list_old)
            code.compli_code_time_dict=all_test_case_time_list_old
            code.simple_code_time_dict=all_test_case_time_list_new
            code_time_list.append(code)

    current_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    util.save_pkl(util.data_root + "iterations_code_time_info/list_comprehension/", str(current_time), code_time_list)
    pro_time_end = time.time()
    print(time.time())
    print("total running time of the program: ", pro_time_end - pro_time_start)

    pass

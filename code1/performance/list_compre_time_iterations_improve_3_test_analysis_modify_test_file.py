import sys,ast,os,csv,time,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
# sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"test_case/")
import util,get_test_case_acc_util,performance_util,configure_pro_envir_util
import code_info
from extract_simp_cmpl_data import ast_util
import ast_performance_util
# import replace_content_by_ast_time_percounter
import performance_replace_content_by_ast_time_percounter


def make_new_test_file(repo_path,me_name, test_html, cl, me,iterations=10):
    relative_test_file = "/".join(test_html.replace("//", "/").split("/")[6:])
    test_full_file_path = repo_path + relative_test_file
    copy_test_full_file_path = "".join([test_full_file_path[:-3], util.copy_file_suffix, ".py"])
    new_test_html = "".join([test_html[:-3], util.copy_file_suffix, ".py"])
    # print("test_html: ", copy_test_full_file_path, test_html, new_test_html, cl, me,
    #       test_full_file_path)

    old_content = util.load_file_path(test_full_file_path)
    # test_code=util.load_file_path(copy_test_full_file_path)
    # print("test_code: ",test_code)
    file_tree = ast.parse(old_content)
    ana_py = ast_performance_util.Fun_Analyzer_Add_Time(me,me_name,iterations)
    file_tree = ana_py.visit(file_tree)
    new_test_code = ast.unparse(file_tree)
    # print("test code of test method: ", file_tree, ana_py.flag)
    # print(ast.unparse(file_tree))
    # print(">>>>>>>>>>>>>>>new_test_code: \n",new_test_html, cl, me,new_test_code)
    util.save_file_path(copy_test_full_file_path, new_test_code)  # copy 一份原来的文件防止失去
    copy_test_full_file_path = "".join([test_full_file_path[:-3], util.copy_file_suffix, ".py"])
    # print(">>>>>>>>>>>>>>>copy_test_full_file_path: \n",copy_test_full_file_path)

    new_test_html = "".join([test_html[:-3], util.copy_file_suffix, ".py"])
    print("test_html: ", copy_test_full_file_path, new_test_html, cl, me,
          test_full_file_path)
    return new_test_html
def code_test_get_time(repo_path,me_name, old_path,old_content,test_me_inf_list,is_pythonic_timeflag=0,is_own_config=0,
                       prefine_cpus="",iterations=10,invo=0,window=4,warms_up=3,threshhold=1,
                       flag_total_test_html=dict(),
                       flag_total_test_html_instances=dict(),
                       num_add_ele_list=[],new_content=""):

    all_valid_flag=1
    # flag_total_test_html=dict()
    # flag_total_test_html_instances=dict()

    all_invocations_time_list = []
    # num_add_ele_list = []
    try:
        # for invo in range(invocations):
        #     print(">>>>>>>come invoca ", invo,len(test_me_inf_list))
            all_test_case_time_list = dict()
        #     one_test_me_inf_list=[]
        #     for test_html, each_rela_path, cl, me in test_me_inf_list:
        #         if me != "test_csv_flyrna":  # 'test_csv_biostats'
        #             continue
        #         one_test_me_inf_list.append((test_html, each_rela_path, cl, me))
        #     test_me_inf_list=one_test_me_inf_list
            for test_html, each_rela_path, cl, me in test_me_inf_list:
                # if me!="test_csv_flyrna":#'test_csv_biostats'
                #     continue
                if (test_html, each_rela_path, cl, me) not in flag_total_test_html:
                    flag_total_test_html[(test_html, each_rela_path, cl, me)]=0
                    flag_total_test_html_instances[(test_html, each_rela_path, cl, me)]=dict()
                # elif flag_total_test_html[(test_html, each_rela_path, cl, me)]:
                #     print(f"all test cases of {(test_html, each_rela_path, cl, me)} has reached steady, its stable invocations (cov of each invocation is less than 0.02 ) reach at {threshhold}")
                #     continue

                fun_list = ["::".join([cl, me]) if cl else me]

                new_test_html = make_new_test_file(repo_path,me_name, test_html, cl, me, iterations)
                # break
                # time.sleep(0.5)
                # util.save_file_path(old_path, new_content)
                if not is_own_config:
                    run_test_result_new = configure_pro_envir_util.run_test_file_capture_output_each_fun(new_test_html,
                                                                                                repo_path,
                                                                                                fun_list=fun_list,
                                                                                                export_python=True,prefine_cpus=prefine_cpus,iterations=iterations)
                else:
                    run_test_result_new = configure_pro_envir_util.run_test_file_capture_output_each_fun(new_test_html, repo_path,
                                                                                                ven_name="venv_zejun_config",
                                                                                                fun_list=fun_list,
                                                                                                export_python=False,prefine_cpus=prefine_cpus,iterations=iterations)
                print(f">>>>>>>>>>{(test_html, each_rela_path, cl, me)} {fun_list} run_test_result_new: ", run_test_result_new)
                if is_pythonic_timeflag:
                    get_time_list = performance_util.get_pythonic_time_list(run_test_result_new)

                else:
                    get_time_list = performance_util.get_time_list(run_test_result_new)
                    # if invo==0:
                    #     num_add_ele = performance_util.get_num_add_ele(run_test_result_new)
                    #     num_add_ele_list.append(num_add_ele)
                # print("get_time_list: ",get_time_list)
                # print("num_add_ele_list: ",num_add_ele_list)
                #'''
                # refactor get_time_list into each instance has iterations number of time
                if len(get_time_list)%iterations!=0:
                    print(f"the number of test case of {test_html} is not a constant")
                    # all_total_time_list.append([])
                    total_time_list=[]
                    all_test_case_time_list[(test_html, each_rela_path, cl, me)] = total_time_list
                    continue
                else:
                    print(">>>>>>>test_case_num: ",len(get_time_list)//iterations)
                if not get_time_list:
                    flag_total_test_html[(test_html, each_rela_path, cl, me)]=2
                    print(f"the time list of code of {old_path} of {test_html}  is []!")
                    # all_total_time_list.append([])
                    total_time_list = []
                    all_test_case_time_list[(test_html, each_rela_path, cl, me)] = total_time_list
                    continue

                test_case_num=len(get_time_list)//iterations
                total_time_list=[[] for i in range(test_case_num)]
                # print(">>>>>>>test_case_num: ",test_case_num)
                if invo == 0 and not is_pythonic_timeflag:
                    num_time_list_instance=[[] for i in range(test_case_num)]
                    num_add_ele = performance_util.get_num_add_ele(run_test_result_new)
                    for i in range(test_case_num):
                        for j in range(iterations):
                            num_time_list_instance[i].append(num_add_ele[test_case_num * j + i])
                    for ind_test_case, ele_list in enumerate(num_time_list_instance):
                        if (test_html, each_rela_path, cl, me) not in num_add_ele_list:
                            num_add_ele_list[(test_html, each_rela_path, cl, me)]=dict()
                        num_add_ele_list[(test_html, each_rela_path, cl, me)][ind_test_case] =ele_list


                for i in range(test_case_num):
                    for j in range(iterations):
                        total_time_list[i].append(get_time_list[test_case_num * j + i])
                # all_total_time_list.append(total_time_list)
                # print(">>>>>>>get_time_list: ", get_time_list)
                # print(">>>>>>>total_time_list: ", total_time_list)

                for ind_test_case,time_list in enumerate(total_time_list):
                    if ind_test_case not in flag_total_test_html_instances[(test_html, each_rela_path, cl, me)]:
                        flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case]=0

                    # elif flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case] >= threshhold:
                    #     continue
                    steady_time_list = [float(e) for e in time_list[warms_up:]]
                    stable_flag = performance_util.whether_cov(steady_time_list, window)
                    print(f"{ind_test_case} instance has {len(steady_time_list)} time, stable_flag: {stable_flag}, ind_test_case: {ind_test_case}",(test_html, each_rela_path, cl, me))
                    flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case]+=stable_flag

                total_valid_flag = 1
                for ind_test_case,time_list in enumerate(total_time_list):
                    if flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case] >= threshhold:
                        continue
                    total_valid_flag = 0
                if total_valid_flag:
                    flag_total_test_html[(test_html, each_rela_path, cl, me)]=1
                    print(f"{test_case_num} test cases of code have reached a stable state in {test_html}")
                    # break
                all_test_case_time_list[(test_html, each_rela_path, cl, me)] = total_time_list
                # time.sleep(10)
                '''
                    # util.save_file_path(old_path, old_content)
                    # old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category_insert_time_complete(
                    #     old_path, for_node,
                    #     assign_node,
                    #     new_tree, remove_ass_flag)
                    # print(">>>>>>>>>>>>>>>>whether timing new content and old content is same: ", flag_same)
                    # # print(new_content)
                    #
                    # util.save_file_path(old_path, new_content)


                print(f"{test_html}, {cl}, {me} all total time list: ",all_total_time_list)
                all_test_case_time_list[(test_html, each_rela_path, cl, me)]=all_total_time_list
                '''
            else:
                flag_success = 1

                util.save_file_path(old_path, old_content)

                print("****************we save the old content to original file: ", old_path)
                #'''
            for test_html, each_rela_path, cl, me in test_me_inf_list:
                if flag_total_test_html[(test_html, each_rela_path, cl, me)]:
                    print(f"all test cases of {(test_html, each_rela_path, cl, me)} has reached steady, its stable invocations (cov of each invocation is less than 0.02 ) reach at {threshhold}")
                    continue
                else:
                    all_valid_flag=0

            # all_invocations_time_list.append(all_test_case_time_list)
    except:
            #'''
            print("****************CODE RUN OCCUR ERRORS")
            util.save_file_path(old_path, old_content)
            print("****************we save the old content to original file: ", old_path)

            #'''
            traceback.print_exc()
    # print(f"{loop_num} loops, total time: {end-start}")
    return all_test_case_time_list,all_valid_flag


if __name__ == '__main__':

    pro_time_start = time.time()
    save_code_info_dir=util.data_root+"performance/list_compre_benchmarks_new_test_single_file_2/"
    save_code_info_dir=util.data_root+"performance/list_compre_benchmarks_new_test_single_file_3/"
    save_code_info_dir=util.data_root+"performance/list_compre_benchmarks_iter_improv_final/"
    save_code_info_dir=util.data_root+"performance/list_compre_benchmarks_iter_improv_final_test/"

    file_dir=util.data_root+"format_code_info/"
    file_name="list_compre"
    code_time_list=[]
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    # invocations = 30
    # threshold = 10
    # iterations = 15
    invocations = 1#50
    threshold = 1#10
    iterations = 2#15
    prefine_cpus="taskset -c 6,7 "
    offset = 0#44#88
    end=44
    for ind_code,code in enumerate(code_info_list[offset:]):
        # if ind_code>0:
        #     break
        code:code_info.CodeInfo
        file_html=code.file_html
        if file_html!="https://github.com/HunterMcGushion/hyperparameter_hunter/tree/master/hyperparameter_hunter/space/space_core.py":#"https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv.py":
            continue
        test_me_inf_list = code.test_case_info_list
        for_node, assign_node, remove_ass_flag, new_tree=code.code_info
        cl,me,repo_name=code.cl,code.me,code.repo_name
        # code.own_config=0
        # print("is ownconfig: ",code.own_config)
        # break
        me_name = me.split("$")[0]
        if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
            print(f"the method name is not valid {me_name}")
            continue
        total_name = get_test_case_acc_util.get_total_name(file_html, cl, me_name)
        repo_path = pro_path + repo_name + "/"
        real_file_html = file_html.replace("//", "/")
        rela_path = real_file_html.split("/")[6:]
        old_path = repo_path + "/".join(rela_path)
        performance_util.backup_content(repo_path, file_html)

        print(f">>>>>>>>>>>>>>>> total_name of {ind_code} code: ", file_html,cl, me_name, total_name)
        flag_total_test_html = dict()
        flag_total_test_html_instances = dict()

        all_invocations_time_list = []
        num_add_ele_list = dict()
        '''
        for invo in range(invocations):
            print(f"*********************invo {invo}*********************************")
            
            old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category_insert_time_complete(old_path,for_node,
                assign_node,
                new_tree, remove_ass_flag)
            print(f">>>>>>>>>>>>>>>>{invo} invocations: whether timing new content and old content is same: ",flag_same)
            # print(new_content)

            util.save_file_path(old_path, new_content)

            # performance_util.backup_time_content(repo_path,file_html,new_content)
            # util.save_file_path(repo_path + rela_path_test_pythonic,
            #                     new_content)
            

            all_test_case_time_list_old,all_valid_flag = code_test_get_time(repo_path, me_name, old_path,
                                                             old_content,
                                                             test_me_inf_list,iterations=iterations,invo=invo,threshhold=threshold,
                                                             flag_total_test_html=flag_total_test_html,
                                                             flag_total_test_html_instances=flag_total_test_html_instances,
                                                             num_add_ele_list=num_add_ele_list,prefine_cpus=prefine_cpus,new_content=new_content)

            print(f"{invo} invocations: all_test_case_time_list_old: ",all_test_case_time_list_old,num_add_ele_list)
            all_invocations_time_list.append(all_test_case_time_list_old)
            if all_valid_flag:
                print(f"the  {ind_code} code has reached steady: ",invo+1)
                print(all_invocations_time_list)
                break
        '''

        flag_total_test_html_pythonic = dict()
        flag_total_test_html_instances_pythonic = dict()

        all_invocations_time_list_pythonic = []
        #'''
        for invo in range(invocations):
            old_content, new_content, flag_same = performance_replace_content_by_ast_time_percounter.replace_file_content_for_compre_3_category(
                old_path, for_node,
                assign_node,
                new_tree, remove_ass_flag)
            print(f"pythonic>>>>>>>>>>>>>>>>{invo} invocations: whether timing new content and old content is same: ",flag_same)

            # print(new_content)

            util.save_file_path(old_path, new_content)
            # performance_util.backup_pythonic_content(repo_path,file_html,new_content)
            # util.save_file_path(repo_path + rela_path_test_pythonic,
            #                     new_content)
            all_test_case_time_list_old, all_valid_flag = code_test_get_time(repo_path, me_name, old_path,
                                                                             old_content,
                                                                             test_me_inf_list, is_pythonic_timeflag=1,iterations=iterations, invo=invo,
                                                                             threshhold=threshold,
                                                                             flag_total_test_html=flag_total_test_html_pythonic,
                                                                             flag_total_test_html_instances=flag_total_test_html_instances_pythonic,
                                                                             num_add_ele_list=num_add_ele_list,
                                                                             prefine_cpus=prefine_cpus,new_content=new_content)

            print(f"pythonic {invo} invocations: all_test_case_time_list_old: ", all_test_case_time_list_old, num_add_ele_list)
            all_invocations_time_list_pythonic.append(all_test_case_time_list_old)
            if all_valid_flag:
                print(f"pythonic the  {ind_code} code has reached steady: ", invo + 1)
                print(all_invocations_time_list_pythonic)
                break


            code_time_list.append(code)
        #'''
        code.flag_total_test_html=flag_total_test_html
        code.flag_total_test_html_instances = flag_total_test_html_instances
        code.flag_total_test_html_pythonic = flag_total_test_html_pythonic
        code.flag_total_test_html_instances_pythonic = flag_total_test_html_instances_pythonic
        code.simple_code_time_dict=all_invocations_time_list
        code.compli_code_time_dict=all_invocations_time_list_pythonic
        code.num_ele_list=num_add_ele_list
        print(f"******************one code pair summary, the index is {ind_code}************************************")
        print(all_invocations_time_list)#,flag_total_test_html,flag_total_test_html_instances)
        print(all_invocations_time_list_pythonic)#, flag_total_test_html_pythonic, flag_total_test_html_instances_pythonic)
        print("num_add_ele_list: ",num_add_ele_list)
        code_info_file_name = total_name + "_" + str(ind_code + offset)
        # util.save_pkl(save_code_info_dir, code_info_file_name, code)
        print(">>>>>>>>>>>>>save successfully! ", save_code_info_dir + code_info_file_name)
        # break
    current_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # util.save_pkl(util.data_root + "iterations_code_time_info/list_comprehension/", str(current_time), code_time_list)
    pro_time_end = time.time()
    print(time.time())
    print("total running time of the program: ", pro_time_end - pro_time_start)

    pass

import copy
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
import performance_replace_content_by_ast_call_star


def make_new_test_file(repo_path, test_html, cl, me, iterations=10):
    relative_test_file = "/".join(test_html.replace("//", "/").split("/")[6:])
    test_full_file_path = repo_path + relative_test_file
    copy_test_full_file_path = "".join([test_full_file_path[:-3], util.copy_file_suffix, ".py"])
    new_test_html = "".join([test_html[:-3], util.copy_file_suffix, ".py"])
    print("test_html: ", copy_test_full_file_path, test_html, new_test_html, cl, me,
          test_full_file_path)

    old_content = util.load_file_path(test_full_file_path)
    # test_code=util.load_file_path(copy_test_full_file_path)
    # print("test_code: ",test_code)
    # file_tree = ast.parse(old_content)
    # ana_py = ast_performance_util.Fun_Analyzer(me,iterations)
    # file_tree = ana_py.visit(file_tree)
    # new_test_code = ast.unparse(file_tree)
    # print("test code of test method: ", file_tree, ana_py.flag)
    # print(ast.unparse(file_tree))
    # print(">>>>>>>>>>>>>>>new_test_code: \n",new_test_html, cl, me,old_content)
    util.save_file_path(copy_test_full_file_path, old_content)  # copy 一份原来的文件防止失去
    copy_test_full_file_path = "".join([test_full_file_path[:-3], util.copy_file_suffix, ".py"])
    new_test_html = "".join([test_html[:-3], util.copy_file_suffix, ".py"])
    # print("test_html: ", copy_test_full_file_path, test_html, new_test_html, cl, me,
    #       test_full_file_path)
    return new_test_html


def code_test_get_time(repo_path, old_path, old_content, test_me_inf_list, is_pythonic_timeflag=0, is_own_config=0,
                       prefine_cpus="", iterations=10, invo=0, window=4, warms_up=3, threshhold=1,
                       flag_total_test_html=dict(),
                       flag_total_test_html_instances=dict(),
                       num_add_ele_list=[], new_content="",pip_install_again=0):
    dict_run_test = dict()
    all_valid_flag = 1
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
            # dict_run_test[test_html]=[]
            print(">>>>>>>>test case info: ",test_html,each_rela_path, cl, me)
            if (test_html, each_rela_path, cl, me) not in flag_total_test_html:
                flag_total_test_html[(test_html, each_rela_path, cl, me)] = 0
                flag_total_test_html_instances[(test_html, each_rela_path, cl, me)] = dict()
            # elif flag_total_test_html[(test_html, each_rela_path, cl, me)]:
            #     print(f"all test cases of {(test_html, each_rela_path, cl, me)} has reached steady, its stable invocations (cov of each invocation is less than 0.02 ) reach at {threshhold}")
            #     continue

            fun_list = ["::".join([cl, me]) if cl else me]

            # new_test_html = make_new_test_file(repo_path, test_html, cl, me, iterations)
            # time.sleep(0.5)
            # util.save_file_path(old_path, new_content)
            if not is_own_config:
                run_test_result_new = configure_pro_envir_util.run_test_file_capture_output_each_fun(test_html,
                                                                                                     repo_path,
                                                                                                     fun_list=fun_list,
                                                                                                     export_python=True,
                                                                                                     prefine_cpus=prefine_cpus,
                                                                                                     iterations=iterations,pip_install_again=pip_install_again)
            else:
                run_test_result_new = configure_pro_envir_util.run_test_file_capture_output_each_fun(test_html,
                                                                                                     repo_path,
                                                                                                     ven_name="venv_zejun_config",
                                                                                                     fun_list=fun_list,
                                                                                                     export_python=False,
                                                                                                     prefine_cpus=prefine_cpus,
                                                                                                     iterations=iterations,pip_install_again=pip_install_again)
            print(f">>>>>>>>>>{(test_html, each_rela_path, cl, me)} {fun_list} run_test_result_new: ")#, run_test_result_new)#)#)
            # dict_run_test[(test_html, each_rela_path, cl, me)] = run_test_result_new
            if is_pythonic_timeflag:
                # get_time_list = performance_util.get_pythonic_time_list(run_test_result_new)
                # get_time_list_test = performance_util.get_pythonic_time_list_two_dimen(run_test_result_new)
                get_time_list = performance_util.get_pythonic_time_list_two_dimen(run_test_result_new)

            else:
                # get_time_list = performance_util.get_time_list(run_test_result_new)
                # get_time_list_test = performance_util.get_time_list_two_dimen(run_test_result_new)
                get_time_list = performance_util.get_time_list_two_dimen(run_test_result_new)

                # if invo==0:
                #     num_add_ele = performance_util.get_num_add_ele(run_test_result_new)
                #     num_add_ele_list.append(num_add_ele)
            print("get_time_list: ",len(get_time_list),len(get_time_list)% iterations)

            # for ind_each,each_test_case in enumerate(get_time_list_test):
            #     print("time info of each_test_case: ",len(each_test_case))
            # print("test_case_num of get_time_list_test: ",len(get_time_list)/iterations)
            # '''
            # refactor get_time_list into each instance has iterations number of time
            if len(get_time_list) % iterations != 0:
                print(f"the number of test case of {test_html} is not a constant")
                # all_total_time_list.append([])
                total_time_list = []
                all_test_case_time_list[(test_html, each_rela_path, cl, me)] = total_time_list
                continue
            else:
                print(">>>>>>>test_case_num: ", len(get_time_list) // iterations)
            if not get_time_list:
                flag_total_test_html[(test_html, each_rela_path, cl, me)] = 2
                print(f"the time list of code of {old_path} of {test_html}  is []!")
                # all_total_time_list.append([])
                total_time_list = []
                all_test_case_time_list[(test_html, each_rela_path, cl, me)] = total_time_list
                continue

            test_case_num = len(get_time_list) // iterations
            total_time_list = [[] for i in range(test_case_num)]
            # print(">>>>>>>test_case_num: ",test_case_num)
            # if invo == 0 and not is_pythonic_timeflag:
            #     num_time_list_instance=[[] for i in range(test_case_num)]
            #     # num_add_ele = performance_util.get_num_add_ele(run_test_result_new)
            #     for i in range(test_case_num):
            #         for j in range(iterations):
            #             num_time_list_instance[i].append(num_add_ele[test_case_num * j + i])
            # for ind_test_case, ele_list in enumerate(num_time_list_instance):
            #     if (test_html, each_rela_path, cl, me) not in num_add_ele_list:
            #         num_add_ele_list[(test_html, each_rela_path, cl, me)]=dict()
            #     num_add_ele_list[(test_html, each_rela_path, cl, me)][ind_test_case] =ele_list
            #

            for i in range(test_case_num):
                for j in range(iterations):
                    total_time_list[i].append(get_time_list[test_case_num * j + i])
            # all_total_time_list.append(total_time_list)
            # print(">>>>>>>get_time_list: ", get_time_list)
            # print(">>>>>>>total_time_list: ", total_time_list)

            for ind_test_case, time_list in enumerate(total_time_list):
                if ind_test_case not in flag_total_test_html_instances[(test_html, each_rela_path, cl, me)]:
                    flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case] = 0

                # elif flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case] >= threshhold:
                #     continue
                # steady_time_list = [float(e) for e in time_list[warms_up:]]
                # stable_flag = performance_util.whether_cov(steady_time_list, window)
                # print(
                #     f"{ind_test_case} instance has {len(steady_time_list)} time, stable_flag: {stable_flag}, ind_test_case: {ind_test_case}",
                #     (test_html, each_rela_path, cl, me))
                flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case] += 1

            total_valid_flag = 1
            for ind_test_case, time_list in enumerate(total_time_list):
                if flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case] >= threshhold:
                    continue
                total_valid_flag = 0
            if total_valid_flag:
                flag_total_test_html[(test_html, each_rela_path, cl, me)] = 1
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
            # '''
        # for test_html, each_rela_path, cl, me in test_me_inf_list:
        #     if flag_total_test_html[(test_html, each_rela_path, cl, me)]:
        #         print(
        #             f"all test cases of {(test_html, each_rela_path, cl, me)} has reached steady, its stable invocations (cov of each invocation is less than 0.02 ) reach at {threshhold}")
        #         continue
        #     else:
        #         all_valid_flag = 0

        # all_invocations_time_list.append(all_test_case_time_list)
    except:
        # '''
        print("****************CODE RUN OCCUR ERRORS")
        util.save_file_path(old_path, old_content)
        print("****************we save the old content to original file: ", old_path)

        # '''
        traceback.print_exc()
    # print(f"{loop_num} loops, total time: {end-start}")
    return all_test_case_time_list, all_valid_flag, dict_run_test



if __name__ == '__main__':

    pro_time_start = time.time()
    save_code_info_dir=util.data_root_mv+"performance/a_call_star_single_2/a_call_star_iter_invoca_2/"
    error_code_dir = util.data_root_mv + "performance/a_call_star_single_2/erro_record_dir_2/"
    time_out_dir=util.data_root_mv + "performance/a_call_star_single_2/time_out_record_dir_2/"
    file_dir=util.data_root+"format_code_info/"
    file_name="call_star_complete"#"multi_ass_sample_317"#"multi_ass_complete"
    code_time_list=[]
    case_is_true_list_filter = []
    time_out_list_filter=[]
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    # invocations = 2
    # threshold = 0
    # iterations = 2
    invocations = 50
    threshold = 50
    iterations = 35
    # invocations = 30
    # threshold = 10
    # iterations = 15
    # invocations = 2#50
    # threshold = 1#10
    # iterations = 2#15
    '''
    >>>>>come here https://github.com/absent1706/sqlalchemy-mixins/tree/master/sqlalchemy_mixins/smartquery.py ('https://github.com/absent1706/sqlalchemy-mixins/tree/master/sqlalchemy_mixins/tests/test_smartquery.py', 'sqlalchemy_mixins.tests.test_smartquery', 'TestSmartQueryAutoEagerLoad', 'test_lazy_dynamic')
    total_time_list_info_dict:  dict_keys([]) https://github.com/kieferk/dfply/tree/master/dfply/reshape.py [['https://github.com/kieferk/dfply/tree/master/test/test_reshape.py', 'test.test_reshape', '', 'test_separate']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/rthalley/dnspython/tree/master/dns/ipv6.py [['https://github.com/rthalley/dnspython/tree/master/tests/test_address.py', 'tests.test_address', 'IPv6Tests', 'test_valid'], ['https://github.com/rthalley/dnspython/tree/master/tests/test_address.py', 'tests.test_address', 'IPv6Tests', 'test_invalid']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/fonttools/fonttools/tree/master/Lib/fontTools/ttLib/tables/C_O_L_R_.py [['https://github.com/fonttools/fonttools/tree/master/Tests/ttLib/tables/C_O_L_R_test.py', 'Tests.ttLib.tables.C_O_L_R_test', 'COLR_V0_Test', 'test_round_trip_xml'], ['https://github.com/fonttools/fonttools/tree/master/Tests/ttLib/tables/C_O_L_R_test.py', 'Tests.ttLib.tables.C_O_L_R_test', 'COLR_V0_Test', 'test_load_from_xml_and_compile'], ['https://github.com/fonttools/fonttools/tree/master/Tests/ttLib/tables/C_O_L_R_test.py', 'Tests.ttLib.tables.C_O_L_R_test', 'COLR_V1_Variable_Test', 'test_round_trip_xml'], ['https://github.com/fonttools/fonttools/tree/master/Tests/ttLib/tables/C_O_L_R_test.py', 'Tests.ttLib.tables.C_O_L_R_test', 'COLR_V1_Test', 'test_round_trip_xml'], ['https://github.com/fonttools/fonttools/tree/master/Tests/ttLib/tables/C_O_L_R_test.py', 'Tests.ttLib.tables.C_O_L_R_test', 'COLR_V1_Test', 'test_load_from_xml_and_compile']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/bpython/bpython/tree/master/bpython/args.py [['https://github.com/bpython/bpython/tree/master/bpython/test/test_args.py', 'bpython.test.test_args', 'TestParse', 'test_version']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/evildmp/BrachioGraph/tree/master//brachiograph.py [['https://github.com/evildmp/BrachioGraph/tree/master//test_brachiograph.py', 'test_brachiograph', '', 'test_test_pattern']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/maxpumperla/elephas/tree/master/elephas/mllib/adapter.py [['https://github.com/maxpumperla/elephas/tree/master/tests/mllib/test_adapter.py', 'tests.mllib.test_adapter', '', 'test_to_matrix']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/rthalley/dnspython/tree/master/dns/renderer.py [['https://github.com/rthalley/dnspython/tree/master/tests/test_renderer.py', 'tests.test_renderer', 'RendererTestCase', 'test_multi_tsig'], ['https://github.com/rthalley/dnspython/tree/master/tests/test_renderer.py', 'tests.test_renderer', 'RendererTestCase', 'test_tsig'], ['https://github.com/rthalley/dnspython/tree/master/tests/test_renderer.py', 'tests.test_renderer', 'RendererTestCase', 'test_basic']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/nccgroup/ScoutSuite/tree/master/ScoutSuite/core/fs.py [['https://github.com/nccgroup/ScoutSuite/tree/master/tests/test_utils_fs.py', 'tests.test_utils_fs', 'TestOpinelFsClass', 'test_read_ip_ranges']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/gmplot/gmplot/tree/master/gmplot/google_map_plotter.py [['https://github.com/gmplot/gmplot/tree/master/tests/test_gmplot.py', 'tests.test_gmplot', 'GoogleMapPlotterTest', 'test_scatter_length_mismatch'], ['https://github.com/gmplot/gmplot/tree/master/tests/test_gmplot.py', 'tests.test_gmplot', 'GoogleMapPlotterTest', 'test_get'], ['https://github.com/gmplot/gmplot/tree/master/tests/test_gmplot.py', 'tests.test_gmplot', 'GoogleMapPlotterTest', 'test_invalid_symbol']]
    total_time_list_info_dict:  dict_keys([]) https://github.com/presslabs/gitfs/tree/master/gitfs/repository.py [['https://github.com/presslabs/gitfs/tree/master/tests/repository/test_repository.py', 'tests.repository.test_repository', 'TestRepository', 'test_comit_no_parents'], ['https://github.com/presslabs/gitfs/tree/master/tests/repository/test_repository.py', 'tests.repository.test_repository', 'TestRepository', 'test_commit_with_nothing_to_commit']]
    '''
    prefine_cpus="taskset -c 2,3 "
    offset = 0
    end=28
    for ind_code,code in enumerate(code_info_list[:]):
        if ind_code not in [63]:
            continue
        one_code_time_start = time.time()
        code:code_info.CodeInfo
        file_html=code.file_html
        # if file_html!="https://github.com/kieferk/dfply/tree/master/dfply/reshape.py":#"https://github.com/absent1706/sqlalchemy-mixins/tree/master/sqlalchemy_mixins/smartquery.py":#"https://github.com/rthalley/dnspython/tree/master/dns/ipv6.py":
        #     continue
        # if file_html!="https://github.com/kieferk/dfply/tree/master/dfply/reshape.py":#"https://github.com/absent1706/sqlalchemy-mixins/tree/master/sqlalchemy_mixins/smartquery.py":#"https://github.com/rthalley/dnspython/tree/master/dns/ipv6.py":
        #     continue
        test_me_inf_list = code.test_case_info_list
        arg_list, new_tree=code.code_info
        old_tree = arg_list[0]
        call_node = arg_list[-2]

        cl,me,repo_name=code.cl,code.me,code.repo_name
        # code.own_config=0
        # print("is ownconfig: ",code.own_config)
        # break
        me_name = me.split("$")[0]
        print(f"me_name is ",me_name)
        if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
            print(f"the method name is not valid {me_name}")
            continue
        total_name = get_test_case_acc_util.get_total_name(file_html, cl, me_name)
        file_name_no_suffix = total_name + "_" + str(ind_code + offset)
        need_configure_flag=0
        # if os.path.exists(save_code_info_dir + file_name_no_suffix + ".pkl"):
        #     lab_code_info = util.load_pkl(save_code_info_dir, file_name_no_suffix)
        #     compli_code_time_dict = lab_code_info.compli_code_time_dict
        #
        #     for key_e in compli_code_time_dict[0]:
        #         if compli_code_time_dict[0][key_e]:
        #
        #             print("yes, I do not need to configure once again", compli_code_time_dict[0])
        #             break
        #     else:
        #         need_configure_flag=0
        #         print("Configure once again")


        repo_path = pro_path + repo_name + "/"
        real_file_html = file_html.replace("//", "/")
        rela_path = real_file_html.split("/")[6:]
        old_path = repo_path + "/".join(rela_path)
        performance_util.backup_content(repo_path, file_html)

        print(f">>>>>>>>>>>>>>>> total_name of {ind_code+offset} code: ", file_html,cl, me_name, total_name)
        flag_total_test_html = dict()
        flag_total_test_html_instances = dict()
        flag_total_test_html_test_one_iter = dict()
        flag_total_test_html_instances_test_one_iter = dict()
        num_add_ele_list_test_one_iter = dict()
        all_invocations_time_list = []
        num_add_ele_list = dict()
        #'''
        # import copy
        # new_callnode=copy.deepcopy(call_node)
        # re_call=performance_replace_content_by_ast_call_star.Rewrite_call(old_tree,new_tree,call_node)
        # re_call.visit(new_callnode)
        print(old_tree[0].lineno,[ast.unparse(e) for e in old_tree],call_node,ast.unparse(call_node),ast.unparse(new_tree))#,ast.unparse(new_callnode)
        #
        old_content, new_content, flag_same = performance_replace_content_by_ast_call_star.replace_content_var_unpack_call_star_insert_time(#replace_content_var_unpack_call_star_insert_time(
            old_path, old_tree, new_tree,call_node, me_name)
        # old_content, new_content, flag_same = performance_replace_content_by_ast_call_star.replace_content_var_unpack_call_star(
        #     old_path, old_tree, new_tree, call_node, me_name)
        # old_content, new_content, flag_same = performance_replace_content_by_ast_call_star.replace_content_var_unpack_call_star(
        #     # replace_content_var_unpack_call_star_insert_time(
        #     old_path, old_tree, new_tree, call_node, me_name)
        # print(old_content)
        # print("***********************")
        print(new_content)
        if flag_same:
            print("there is no difference code  ", file_html, cl, me_name, total_name)
            case_is_true_list_filter.append([ind_code,ind_code+offset, "complicated code", file_html, cl, me_name, total_name])
            break
            continue
        break

        # old_content, new_content, flag_same = performance_replace_content_by_ast_call_star.replace_content_var_unpack_call_star(
        #     old_path, old_tree, new_tree, call_node, me_name)
        # print(f">>>>>>>>>>>>>>>>{invo} invocations: whether timing new content and old content is same: ", flag_same)
        # util.save_file_path(old_path, new_content)
        # print(new_content)
        # print("new_tree: ",ast.unparse(new_tree))
        # print(test_me_inf_list)
        '''
        util.save_file_path(old_path, new_content)
        one_invo_start = time.time()
        print("code.own_config: ",code.own_config)
        all_test_case_time_list_old, all_valid_flag, dict_run_test_complicated = code_test_get_time(repo_path,
                                                                                                    old_path,
                                                                                                    old_content,
                                                                                                    test_me_inf_list,
                                                                                                    is_pythonic_timeflag=0,
                                                                                                    is_own_config=code.own_config,
                                                                                                    iterations=1,
                                                                                                    invo=1,
                                                                                                    threshhold=threshold,
                                                                                                    flag_total_test_html=flag_total_test_html_test_one_iter,
                                                                                                    flag_total_test_html_instances=flag_total_test_html_instances_test_one_iter,
                                                                                                    num_add_ele_list=num_add_ele_list_test_one_iter,
                                                                                                    prefine_cpus=prefine_cpus,
                                                                                                    new_content=new_content,pip_install_again=need_configure_flag)
        one_invo_end = time.time()
        # print(all_test_case_time_list_old)
        # break

        for key_e in all_test_case_time_list_old:
            if all_test_case_time_list_old[key_e]:
                print("yes, there is time", file_html, cl, me_name, total_name)
                break
        else:
            print("There is no time", file_html, cl, me_name, total_name)
            continue
        if one_invo_end - one_invo_start > 15:
            print("the test case run too long ", one_invo_end - one_invo_start)
            # if time_out_flag:
            time_out_list_filter.append(
                    [ind_code, ind_code + offset, "complicated code", file_html, cl, me_name, total_name])
                # continue
            # time_out_flag = 1
            continue

        

        all_invocations_res=dict()
        for invo in range(invocations):

            print(f"*********************invo {invo}*********************************")
            

            # performance_util.backup_time_content(repo_path,file_html,new_content)
            # util.save_file_path(repo_path + rela_path_test_pythonic,
            #                     new_content)

            util.save_file_path(old_path, new_content)
            all_test_case_time_list_old,all_valid_flag,dict_run_test_complicated = code_test_get_time(repo_path, old_path,
                                                             old_content,
                                                             test_me_inf_list,is_pythonic_timeflag=0,is_own_config=code.own_config,iterations=iterations,invo=invo,threshhold=threshold,
                                                             flag_total_test_html=flag_total_test_html,
                                                             flag_total_test_html_instances=flag_total_test_html_instances,
                                                             num_add_ele_list=num_add_ele_list,prefine_cpus=prefine_cpus,new_content=new_content)


            # print(f"{invo} invocations: all_test_case_time_list_old: ",all_test_case_time_list_old,num_add_ele_list)
            all_invocations_time_list.append(all_test_case_time_list_old)

            # print("dict_run_test_complicated: ",dict_run_test_complicated)
            # all_invocations_res[invo]=dict_run_test_complicated
        # code.set_run_test_res_compli_code(all_invocations_res)
        # code_info_file_name = total_name + "_" + str(ind_code + offset)
        # print("all_invocations_time_list: ",len(all_invocations_time_list))
        # util.save_pkl(save_code_info_dir, code_info_file_name, code)

        
            # if all_valid_flag:
            #     print(f"the  {ind_code} code has reached steady: ",invo+1)
            #     print(all_invocations_time_list)
            #     break
        
        flag_total_test_html_pythonic = dict()
        flag_total_test_html_instances_pythonic = dict()

        all_invocations_time_list_pythonic = []
        all_invocations_res_pythonic = dict()
        # print("new_tree: ",old_tree,new_tree)
        old_content, new_content, flag_same = performance_replace_content_by_ast_call_star.replace_content_var_unpack_call_star(
            old_path, old_tree, new_tree,call_node, me_name)
        if flag_same:
            print("there is no difference pythonic code  ", file_html, cl, me_name, total_name)
            case_is_true_list_filter.append([ind_code, "pythonic code", file_html, cl, me_name, total_name])
            continue

        # print(f"pythonic>>>>>>>>>>>>>>>>{invo} invocations: whether timing new content and old content is same: ",
        #       flag_same)
        # util.save_file_path(old_path, new_content)
        # print(new_content)

        for invo in range(invocations):
            print(f"*********************invo {invo}*********************************")

            util.save_file_path(old_path, new_content)
            # performance_util.backup_pythonic_content(repo_path,file_html,new_content)
            # util.save_file_path(repo_path + rela_path_test_pythonic,
            #                     new_content)
            all_test_case_time_list_old, all_valid_flag,dict_run_test = code_test_get_time(repo_path, old_path,
                                                                             old_content,
                                                                             test_me_inf_list, is_pythonic_timeflag=1,is_own_config=code.own_config,iterations=iterations, invo=invo,
                                                                             threshhold=threshold,
                                                                             flag_total_test_html=flag_total_test_html_pythonic,
                                                                             flag_total_test_html_instances=flag_total_test_html_instances_pythonic,
                                                                             num_add_ele_list=num_add_ele_list,
                                                                             prefine_cpus=prefine_cpus,new_content=new_content)

            # all_invocations_res_pythonic[invo]=dict_run_test
            # print(f"pythonic {invo} invocations: all_test_case_time_list_old: ", all_test_case_time_list_old, num_add_ele_list)
            all_invocations_time_list_pythonic.append(all_test_case_time_list_old)
            # if all_valid_flag:
            #     print(f"pythonic the  {ind_code} code has reached steady: ", invo + 1)
            #     # print(all_invocations_time_list_pythonic)
            #     break

        # print("all_invocations_time_list_pythonic: ", all_invocations_time_list_pythonic)
            # code_time_list.append(code)
        # code.set_run_test_res_simple_code(all_invocations_res_pythonic)

        code.flag_total_test_html=flag_total_test_html
        code.flag_total_test_html_instances = flag_total_test_html_instances
        code.flag_total_test_html_pythonic = flag_total_test_html_pythonic
        code.flag_total_test_html_instances_pythonic = flag_total_test_html_instances_pythonic
        code.simple_code_time_dict=all_invocations_time_list
        code.compli_code_time_dict=all_invocations_time_list_pythonic
        code.num_ele_list=num_add_ele_list
        print(f"******************one code pair summary, the index is {ind_code}************************************")
        print("len(all_invocations_time_list): ",len(all_invocations_time_list))#,flag_total_test_html,flag_total_test_html_instances)
        print("len(all_invocations_time_list_pythonic): ",len(all_invocations_time_list_pythonic))#, flag_total_test_html_pythonic, flag_total_test_html_instances_pythonic)
        print("num_add_ele_list: ",num_add_ele_list)
        # break
        
        code_info_file_name = total_name + "_" + str(ind_code + offset)
        util.save_pkl(save_code_info_dir, code_info_file_name, code)
        one_code_time_end = time.time()
        print(">>>>>>>>>>>>>save successfully! ", save_code_info_dir + code_info_file_name,one_code_time_end-one_code_time_start)
        # break
        
    current_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    util.save_pkl(error_code_dir, "error_code_is_true_info", case_is_true_list_filter)
    util.save_pkl(time_out_dir, "time_out_code_info", time_out_list_filter)
'''
    pro_time_end = time.time()
    print(time.time())
    print("total running time of the program: ", pro_time_end - pro_time_start)

    pass

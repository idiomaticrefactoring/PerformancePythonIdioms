import sys, ast, os, csv, time, traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + "performance/")
# sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir + "test_case/")
sys.path.append(code_dir +"transform_c_s/")
import complicated_code_util
from extract_simp_cmpl_data import ast_util
import util, get_test_case_acc_util, performance_util, configure_pro_envir_util
import code_info,copy
def get_idiom_assign_multi(tree):
    code_list = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets_str_list=[]
            value_str_list=[]
            targets=node.targets
            num_tar=0
            if len(targets)==1:
                if isinstance(targets[0], (ast.Tuple, ast.List)):
                    for e_t in targets[0].elts:
                        targets_str_list.append(ast.unparse(e_t))
                else:
                    return code_list
                # num_tar+=ast_util.get_basic_count(t)
            value=node.value
            if isinstance(value, (ast.Tuple, ast.List)):
                for cur in value.elts:
                    value_str_list.append(ast.unparse(cur))
            else:
                return code_list
            if len(targets_str_list)>1<len(value_str_list)==len(targets_str_list) and len(set(targets_str_list)&set(value_str_list))==len(set(targets_str_list)):
                ass_list=[]
                for ind_t,e in enumerate(targets_str_list[:-1]):
                    ass_list.append( "tempory_"+str(ind_t+1)+"="+e)
                    ass_list.append(e+"="+value_str_list[ind_t])
                ass_list.append(targets_str_list[-1]+"="+"tempory_"+str(len(targets_str_list)-1))
                code_list.append([ass_list,node])

            # num_value=ast_util.get_basic_count(value)
            # if num_value==num_tar>1:
            #     code_list.append([ast.unparse(node),num_value])
    return code_list

def save_repo_for_else_complicated(repo_name):
    count_complicated_code=0
    print("come the repo: ", repo_name)
    one_repo_for_else_code_list = []
    dict_file = dict()
    for file_info in dict_repo_file_python[repo_name]:

        file_path = file_info["file_path"]
        # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
        #     continue
        file_html = file_info["file_html"]

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
                    print("come this file: ", file_html)
                    print(code_list)
                    # intersect_list.append(repo_name)
                if code_list:
                    ast_util.set_dict_class_code_list(tree, dict_class, class_name, code_list)

            #print("func number: ",file_html,len(ana_py.func_def_list))
            # for tree in ana_py.func_def_list:
            #     #print("tree_ func_name",tree.__dict__)
            #     code_list.extend(get_idiom_assign_multi(tree))
            # if code_list:
            #         one_repo_for_else_code_list.append([code_list, file_path, file_html])
            if dict_class:
                print(dict_class)
                dict_file[file_html] = dict_class
        except SyntaxError:
            print("the file has syntax error")
            continue
        except ValueError:

            traceback.print_exc()

            print("the file has value error: ", file_html)

            continue
        #break
    if 1:#dict_file:
        # count_complicated_code=count_complicated_code+len(one_repo_for_else_code_list)
        # print("it exists for else complicated code1: ", len(one_repo_for_else_code_list))
        # util.save_pkl(save_complicated_code_dir_pkl,repo_name,dict_file)
        util.save_pkl(save_complicated_code_dir_pkl, repo_name, dict_file)

        # util.save_json(save_complicated_code_dir, repo_name, dict_file)
        #print("save successfully! ", save_complicated_code_dir + repo_name)
        pass

    return count_complicated_code
def get_test_case(test_case_complicate_code,dict_comp_file,file_html):
    test_me_inf_list=[]
    dict_me_test_me_pair= dict()
    com_dict_me = dict_comp_file[file_html]
    all_full_me_list = list(com_dict_me.keys())
    if not all_full_me_list:
        return dict_me_test_me_pair
    com_file_name=file_html.split("/")[-1][:-3]
    # print("code1 file_html: ", file_html, all_full_me_list)
    for file_name in test_case_complicate_code:
        #{"complica_num":0,"test_pair":[]}
        #matchzoo.preprocessors.units.WordPieceTokenize.transform
        #matchzoo.preprocessors.units.tokenize.WordPieceTokenize.transform'
        # print("all code1 methods: ",all_full_me_list)
        for test_case_html in test_case_complicate_code[file_name]:
            # if test_case_html!="https://github.com/NTMC-Community/MatchZoo/tree/master/tests/unit_test/processor_units/test_processor_units.py":
            #     continue

            # print("test case code1 file_html: ", test_case_html)
            dict_class=test_case_complicate_code[file_name][test_case_html]
            for cl in dict_class:
                for me in dict_class[cl]:
                    # print("test_method: ",cl, me)
                    api_list = dict_class[cl][me]
                    # print("all apis: ", api_list,all_full_me_list)
                    # it shows whether the me is be tested by the  api_list
                    def get_intersect(all_full_me_list,api_list):

                        intersect_methods=[]
                        all_new_full_me_list = copy.deepcopy(all_full_me_list)
                        for ind in range(len(all_full_me_list[0].split("."))-1):
                            for ind_me,full_me in enumerate(all_new_full_me_list):
                                if ind_me in intersect_methods:
                                    continue
                                del_file_name_full_me=full_me[::-1].replace("."+com_file_name[::-1],"",1)
                                # print("del_file_name_full_me: ",full_me[::-1],"."+com_file_name[::-1],del_file_name_full_me[::-1])
                                if full_me in api_list or del_file_name_full_me[::-1] in api_list:
                                    intersect_methods.append(ind_me)
                                    # print(">>>>>>>>>>yes intersect: ",full_me,all_full_me_list,api_list)
                            # if intersect_methods:
                            #     break
                            all_new_full_me_list=[".".join(full_me.split(".")[ind+1:]) for full_me in all_full_me_list ]
                            # print("all_new_full_me_list: ",all_new_full_me_list)
                        # if intersect_methods:
                        #     print("*********************all_full_me_list: ", all_full_me_list)
                        return intersect_methods


                    intersect=get_intersect(all_full_me_list, api_list)


                    if intersect:#set(all_full_me_list) & set(api_list):
                        flag_repo=1
                        print("intersect: ",test_case_html,cl,me)
                        for ind in intersect:
                            full_me=all_full_me_list[ind]
                            # "https://github.com/airspeed-velocity/asv/tree/master/"

                            test_me_inf_list.append([test_case_html,".".join(file_html.split("/")[8:]), cl,me])

                            if full_me in dict_me_test_me_pair:

                                dict_me_test_me_pair[full_me]["test_pair"].append([test_case_html,cl,me])
                            else:
                                dict_me_test_me_pair[full_me] = dict()
                                dict_me_test_me_pair[full_me]["complica_num"] = com_dict_me[full_me]
                                dict_me_test_me_pair[full_me]["test_pair"] = [[test_case_html,cl,me]]
                            # count_code+=com_dict_me[full_me]
                            # count_me+=1

                            # print(
                            #     f"method {full_me}  of {file_html} exist test case {me} in {test_case_html}")
                            #             b
    return dict_me_test_me_pair,test_me_inf_list
def transform_me_full_name(save_for_else_complicated_code_dir_pkl, save_for_else_methods_dir):
    count_repo, file_count, me_count, code_count = 0, 0, 0, 0
    all_count_repo, all_file_count, all_me_count = 0, 0, 0
    all_repo_no_test_count,all_file_no_test_count, all_me_no_test_count, all_code_no_test_count=0, 0, 0, 0
    for file_name in os.listdir(save_for_else_complicated_code_dir_pkl):
        all_count_repo+=1
        repo_name = file_name[:-4]
        dict_comp_file = dict()
        # test_case_complicate_code = util.load_pkl(save_test_methods_dir, repo_name)
        # files_num_list.append(repo_files_info[repo_name])
        # star_num_list.append(repo_star_info[repo_name])
        # contributor_num_list.append(repo_contributor_info[repo_name])

        complicate_code = util.load_pkl(save_for_else_complicated_code_dir_pkl, repo_name)

        repo_file_count, repo_me_count, repo_code_count, repo_all_file_count, repo_all_me_count,file_no_test_count, me_no_test_count, code_no_test_count = complicated_code_util.get_code_count_contain_test(
            complicate_code)

        count_repo+= 1 if repo_me_count else 0
        repo_exist = 0
        all_file_no_test_count+=file_no_test_count
        all_me_no_test_count+=me_no_test_count
        all_code_no_test_count+=code_no_test_count
        code_count += repo_code_count
        file_count += repo_file_count
        me_count += repo_me_count
        all_file_count += repo_all_file_count
        all_me_count += repo_all_me_count
        for file_html in complicate_code:

            map_file_name = file_html.split("/")[-1][:-3]
            # filter out test files
            if map_file_name.startswith("test_") or map_file_name.endswith("_test"):
                continue
            #             if map_file_name not in dict_comp_file:
            #                 dict_comp_file[map_file_name] = dict()
            dict_class = dict()
            real_file_html = file_html.replace("//", "/")
            rela_path = ".".join(real_file_html.split("/")[6:-1])
            exist_total_name=set([])
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if not complicate_code[file_html][cl][me]:
                        continue
                    repo_exist = 1
                    me_name = me.split("$")[0]
                    if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
                        continue
                    if rela_path:
                        total_name = ".".join([rela_path, map_file_name, cl, me_name])
                    else:
                        total_name = ".".join([map_file_name, cl, me_name])
                    total_name = total_name.replace("..", ".")
                    if total_name in dict_class:
                        exist_total_name.add(total_name)
                        print("it is possible! because the same file define two same functions", total_name,
                              dict_class[total_name], file_html)
                        dict_class[total_name] += dict_class[total_name]
                        # dict_class[total_name].append([len(complicate_code[file_html][cl][me]),file_html])

                    else:
                        dict_class[total_name] = len(complicate_code[file_html][cl][me])  # ,file_html]
                        # dict_class[total_name] =[len(complicate_code[file_html][cl][me]),file_html]
            for e in exist_total_name:
                del dict_class[e]
            dict_comp_file[file_html] = dict_class
        print(dict_comp_file)
        util.save_pkl(save_for_else_methods_dir, repo_name, dict_comp_file)
        all_repo_no_test_count += repo_exist
        # complicate_code = util.load_pkl(save_for_else_complicated_code_dir_pkl, repo_name)
    print("count: ", count_repo,file_count, me_count, code_count,  all_count_repo, all_file_count, all_me_count)
    # 提取的complicated code中不包含test文件的信息
    print("no test count: ", all_repo_no_test_count, all_file_no_test_count, all_me_no_test_count,all_code_no_test_count)

if __name__ == '__main__':
    file_dir = util.data_root + "format_code_info/"
    file_name = "multi_ass_sample_317"  # "multi_ass_complete"
    save_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl/multi_assign_idiom_code_swap/"
    dict_repo_file_python= util.load_json(util.data_root, "python3_1000repos_files_info")

    save_code_info_dir=util.data_root+"performance/a_multi_assign/a_multi_assign_iter_invoca/"
    code_info_list = util.load_pkl(file_dir, file_name)
    repo_name_list= ['skidl', 'networkx','graphite-api','pygorithm','XlsxWriter', 'cms', 'more-itertools', 'opytimizer']#
    # for ind_code,code in enumerate(code_info_list[:]):
    #     # if ind_code not in [1]:
    #     #     continue
    #     one_code_time_start = time.time()
    #     code:code_info.CodeInfo
    #     file_html=code.file_html
    #     # if file_html!="https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv.py":
    #     #     continue
    #     test_me_inf_list = code.test_case_info_list
    #     old_tree, new_tree=code.code_info
    #     cl,me,repo_name=code.cl,code.me,code.repo_name
    #     repo_name_list.append(repo_name)
    # print("len: ",len(repo_name_list),len(set(repo_name_list)))
    '''
    file_dir = util.data_root + "format_code_info/"
    file_name="multi_ass_complete"#"chain_compare_complete"
    code_info_list = util.load_pkl(file_dir, file_name)
    for ind_code,code in enumerate(code_info_list):
        # if ind_code not in [1]:
        #     continue

        code:code_info.CodeInfo

        cl,me,repo_name=code.cl,code.me,code.repo_name
        repo_name_list.append(repo_name)
    print("len: ", len(repo_name_list), len(set(repo_name_list)))
    '''
    # intersect_list=[]
    for repo_name in set(repo_name_list):
        save_repo_for_else_complicated(repo_name)


    save_for_else_methods_dir=util.data_root+"performance/a_multi_assign/a_multi_assign_iter_invoca/"
    save_me_test_me_dir= util.data_root + "methods_test_method_pair/multip_assign_complicated/"
    save_for_else_methods_dir = util.data_root + "methods/multip_assign_complicated_new_swap/"
    transform_me_full_name(save_complicated_code_dir_pkl, save_for_else_methods_dir)
    def save_me_test_me(repo_name,list_code_info_list):
        dict_intersect_test_methods=dict()
        save_test_methods_dir = util.data_root + "test_case/"
        test_case_complicate_code = util.load_pkl(save_test_methods_dir, repo_name)
        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)
        dict_comp_file = util.load_pkl(save_for_else_methods_dir, repo_name)

        # print("come the repo to search test methods: ", repo_name)
        # if repo_name!="bert":#"MatchZoo":
        #     continue
        # print("存在相同的文件名存在test case 需要进一步确定 多个相同的文件名时, 到底测试文件测试的是哪一个文件: ",file_name)
        for file_html in dict_comp_file:
            # print("same file_html: ",repo_name,file_html)

            # if file_html!="https://github.com/google-research/bert/tree/master//tokenization.py":#"https://github.com/NTMC-Community/MatchZoo/tree/master/matchzoo/preprocessors/units/tokenize.py":
            #     continue
            for cl in dict_comp_file:
                for me in dict_comp_file[cl]:
                    print("cl,me: ",cl,"---",me)
                    print("complicate_code: ", complicate_code[file_html])
                    for key in complicate_code[file_html]:
                        for me_code in complicate_code[file_html][key]:
                            if me.split(".")[-1] == me_code.split("$")[0] and key=='':
                                dict_me_test_me_pair, test_me_inf_list = get_test_case(test_case_complicate_code,
                                                                                       dict_comp_file, file_html)
                                if test_me_inf_list:
                                    code_list = complicate_code[file_html][key][me_code]
                                    for ass_list, new_tree_content in code_list:
                                        code_info_cla = code_info.CodeInfo(repo_name, file_html, '', me,
                                                                           [ass_list, new_tree_content], test_me_inf_list)
                                        list_code_info_list.append(code_info_cla)

                            elif me.split(".")[-1] == me_code.split("$")[0] and key==me.split(".")[-2]:
                                dict_me_test_me_pair, test_me_inf_list = get_test_case(test_case_complicate_code,
                                                                                       dict_comp_file, file_html)
                                if test_me_inf_list:
                                    code_list = complicate_code[file_html][key][me_code]
                                    for ass_list, new_tree_content in code_list:
                                        code_info_cla = code_info.CodeInfo(repo_name, file_html, me.split(".")[-2], me,
                                                                           [ass_list, new_tree_content], test_me_inf_list)
                                        list_code_info_list.append(code_info_cla)
                                                                       #                                        test_me_inf_list)

                                # if file_html not in complicate_code:
                    #     continue
                    # code_list=complicate_code[file_html][cl][me.split("$")[0]]
                    # for ass_list, new_tree_content in dict_comp_file[cl][me]:
                    #                 dict_me_test_me_pair,test_me_inf_list = get_test_case(test_case_complicate_code, dict_comp_file, file_html)
                        # if dict_me_test_me_pair:
                        #     code_info_cla = code_info.CodeInfo(repo_name, file_html, cl, me, [ass_list, new_tree_content],
                        #                                        test_me_inf_list)
                        # print(">>>>>test case info: ", [ass_list, new_tree_content],test_me_inf_list)

                    # if dict_me_test_me_pair:
                    #     dict_intersect_test_methods[file_html] = dict_me_test_me_pair
        # if dict_intersect_test_methods:
        #     util.save_pkl(save_me_test_me_dir, repo_name, dict_intersect_test_methods)

    count_instance=0
    list_code_info_list=[]
    for repo_name in set(repo_name_list):
        save_me_test_me(repo_name,list_code_info_list)
    util.save_pkl(util.data_root + "format_code_info/", "multi_ass_swap", list_code_info_list)

    #skidl, networkx,graphite-api,pygorithm
    # test_me_inf_list=[]
    #
    # for repo_name in set(repo_name_list):
    #     save_me_test_me(repo_name)
    #'''
    # pool = newPool(nodes=30)
    # pool.map(save_me_test_me, list(dict_repo_file_python.keys()))  # [:3]sample_repo_url ,token_num_list[:1]
    # pool.close()
    # pool.join()

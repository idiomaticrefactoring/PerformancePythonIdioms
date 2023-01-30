# compute FanIn
# compute num of APIs from third parties
# write method code into csv file to check
import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
sys.path.append(code_dir+"hityper/")
sys.path.append(code_dir+"wrap_refactoring/")
from hityper.tdg_generator import TDGGenerator
from hityper.utils import formatUserTypes, getRecommendations, test_multiplefile
from hityper.usertype_finder import UsertypeFinder
from hityper.config import config
from hityper import logger
from hityper.utils import detectChange, SimModel
import logging
import util,re
import util_perf
from code_info import CodeInfo
from extract_simp_cmpl_data import ast_util
import pandas as pd
import numpy as np

from math import log
import scipy as sp

from scipy import stats

from sklearn import preprocessing
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

#from sklearn.cross_validation import train_test_split

import statsmodels.formula.api as smf
import seaborn as sns

import warnings
def get_data_type():
    count_code = 0
    count_instance = 0
    count_test_me = 0
    count_var_null=0
    dict_pd=dict()
    for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):

        file_name_no_suffix = file_name[:-4]
        # size_obj_dict = util.load_pkl(sizeof_code_info_dir, file_name_no_suffix)
        # print("size_obj_dict: ",size_obj_dict)
        # break
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: CodeInfo
        for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
        cl = lab_code_info.cl
        me = lab_code_info.me
        me_name=me.split("$")[0]
        repo_name = lab_code_info.repo_name
        # test_me_inf_list=lab_code_info.test_me_inf_list
        pro_path = util.data_root + "python_star_2000repo/"
        repo_path = pro_path + repo_name + "/"
        file_html = lab_code_info.file_html
        if file_html!="https://github.com/maxpumperla/betago/tree/master/betago/model.py":#"https://github.com/tanghaibao/goatools/tree/master/goatools/nt_utils.py":#"https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/systemctl_luf.py":#"https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv.py":
            continue
        dynamic_info_dict = util.load_pkl(dynamic_code_info_dir, file_name_no_suffix)
        size_obj_dict = dynamic_info_dict['size']
        vars_info_dict = dynamic_info_dict['var']
        print("vars_info_dict: ",vars_info_dict)
        total_time_list_info_dict = lab_code_info.total_time_list_info_dict
        if not total_time_list_info_dict:
            continue
        for test_me in total_time_list_info_dict:
            count_test_me += 1
            for instance in total_time_list_info_dict[test_me]:
                instance_feature = total_time_list_info_dict[test_me][instance]
                if test_me not in vars_info_dict or instance not in vars_info_dict[test_me]:
                    count_var_null += 1
                    continue
                one_instance_var_dict=vars_info_dict[test_me][instance]
                for key in one_instance_var_dict:
                        print("value: ",one_instance_var_dict[key])
                        pattern = re.compile("'(.*)'")
                        var_type = pattern.findall(one_instance_var_dict[key])[0]
                        print("str: ",var_type)
                        if var_type not in util_perf.builtins_types and "builtin" not in var_type:
                                if "expVar" not in dict_pd:
                                        dict_pd['expVar'] = 0

                                dict_pd['expVar']+=1
                        if 'method' in var_type:
                                if "FanIn" not in dict_pd:
                                        dict_pd['FanIn'] = 0

                                dict_pd['FanIn']+=1
                        if 'method' == var_type:
                                if "externalCall" not in dict_pd:
                                        dict_pd['externalCall'] = 0

                                dict_pd['externalCall']+=1




                # if "expVar" not in dict_pd:
                #         dict_pd['expVar'] = [lab_code_info.get_code_str()]
                # else:
                #         dict_pd['expVar'].append(lab_code_info.get_code_str())
                # if "expCall" not in dict_pd:
                #         dict_pd['expCall'] = [lab_code_info.get_code_str()]
                # else:
                #         dict_pd['expCall'].append(lab_code_info.get_code_str())


                print(f">>>>>>>>>>{test_me} of {instance} in vars_info_dict:\n", vars_info_dict[test_me][instance])
        print("come the file_name: ", ind, file_name,file_html,me,count_var_null)
        '''
        real_file_html = file_html.replace("//", "/")
        rela_path = real_file_html.split("/")[6:]
        file_path = repo_path + "/".join(rela_path)
        try:
            content = util.load_file_path(file_path)
            print(content)
        except:
            print(f"{file_path} is not existed!")
            continue
        file_tree = ast.parse(content)
        me_tree=None
        ana_py = ast_util.Fun_Analyzer()
        ana_py.visit(file_tree)
        for tree, class_name in ana_py.func_def_list:
            fun_name=tree.name
            if fun_name==me_name:
                me_tree=tree
                print(">>>>>method code:\n",ast.unparse(me_tree))
                break
        root = ast.parse(content)
        print(file_path,repo_path)
        if config["simmodel"] != None:
            simmodel = SimModel(config[config["simmodel"]], config["tokenizer"])
        else:
            simmodel = None
        usertypefinder=UsertypeFinder(file_path,repo_path[:-1],False)
        usertypes, _ = usertypefinder.run(root)
        print(usertypes)
        type4py=True
        recommendations=None
        generator = TDGGenerator(file_path, optimize=True, locations=None, usertypes=usertypes, alias=1, repo=repo_path[:-1])
        global_tg = generator.run(root)
        print()
        str_results = {}
        global_tg.passTypes(debug=False)
        str_results["global@global"] = global_tg.dumptypes()
        if recommendations == None and type4py:
                recommendations = getRecommendations(content)
        elif isinstance(recommendations, dict) and file_path in recommendations:
                recommendations = recommendations[file_path]
        print("recommendations: ",recommendations)
        for tg in global_tg.tgs:
                if recommendations != None:
                        changed = True
                        iters = 0
                        while changed and iters < config["max_recommendation_iteration"]:
                                iters += 1
                                tg.passTypes(debug=False)
                                types = tg.findHotTypes()
                                tg.recommendType(types, recommendations, formatUserTypes(usertypes),
                                                 usertypes["module"], 1, simmodel=simmodel)
                                tg.passTypes(debug=False)
                                new_types = tg.findHotTypes()
                                changed = detectChange(types, new_types)
                                tg.simplifyTypes()
                else:
                        tg.passTypes(debug=False)
                        tg.simplifyTypes()
                str_results[tg.name] = tg.dumptypes()
                # with open(outputrepo + "/" + args.source.replace("/", "_").replace(".py",
                #                                                                    "_INFERREDTYPES.json"),
                #           "w", encoding="utf-8") as of:
                #         of.write(json.dumps(str_results, sort_keys=True, indent=4,
                #                             separators=(',', ': ')))
                # logger.info("Saved results to {}".format(
                #         outputrepo + "/" + args.source.replace("/", "_").replace(".py",
                #                                                                  "_INFERREDTYPES.json")))
        print("result: ",str_results)
        '''
    # except Exception as e:
    # traceback.print_exc()
    # logger.error("Type inference failed for file {}, reason: {}".format(args.source, e))
def save_features():
        dict_pd = dict()
        count_code=0
        count_instance=0
        count_test_me=0
        count_size_of_null=0
        # '''
        # 第9个data:  {'num_ele': [0, 2], 'perf_change': [1.5406070811248669, 0.950779229519387], 'num_loop': [1, 1], 'num_if': [1, 1], 'num_if_else': [0, 0], 'num_func_call': [2, 2], 'num_param': [2, 2], 'num_var': [7, 7], 'num_List': [1, 1], 'num_Dict': [0, 0], 'num_Set': [0, 0], 'num_Tuple': [0, 0], 'num_Subscript': [0, 0], 'num_Slice': [0, 0], 'num_Attr': [2, 2], 'num_constant': [1, 1], 'num_line': [4, 4], 'num_Keywords': [5, 5], 'num_Operators': [0, 0], 'num_Delimiters': [11, 11]}
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                print("file_name: ", ind,file_name)
                file_name_no_suffix = file_name[:-4]
                size_obj_dict = util.load_pkl(sizeof_code_info_dir, file_name_no_suffix)
                # print("size_obj_dict: ",size_obj_dict)
                # break
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: CodeInfo
                for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
                # cl=lab_code_info.cl
                # me=lab_code_info.me
                # repo_name=lab_code_info.repo_name
                # pro_path = util.data_root + "python_star_2000repo/"
                # repo_path = pro_path + repo_name + "/"
                # file_html=lab_code_info.file_html
                # real_file_html = file_html.replace("//", "/")
                # rela_path = real_file_html.split("/")[6:]
                # file_path = repo_path + "/".join(rela_path)
                # try:
                #     content = util.load_file_path(file_path)
                # except:
                #     print(f"{file_path} is not existed!")
                #     continue
                # file_tree = ast.parse(content)
                # ana_py = ast_util.Fun_Analyzer()
                # ana_py.visit(file_tree)
                # dict_class = dict()
                # for tree, class_name in ana_py.func_def_list:
                # print("total_time_list_info_dict: ",lab_code_info.total_time_list_info_dict)
                total_time_list_info_dict=lab_code_info.total_time_list_info_dict
                if not total_time_list_info_dict:
                        continue
                new_node_list = [new_tree]
                if not remove_ass_flag:
                        new_node_list.append(assign_node)
                dict_features = util_perf.get_features([for_node, assign_node])  # .get_features()

                # print("features: ", ast.unparse(for_node), "\n", ast.unparse(assign_node))
                # print("features: ", dict_features)
                one_code_num_list=[]
                for test_me in total_time_list_info_dict:
                        count_test_me+=1
                        for instance in total_time_list_info_dict[test_me]:
                                instance_feature=total_time_list_info_dict[test_me][instance]
                                if test_me not in size_obj_dict or instance not in size_obj_dict[test_me]:
                                        count_size_of_null+=1
                                        continue
                                if "file_html" not in dict_pd:
                                        dict_pd["file_html"] = [lab_code_info.file_html]
                                else:
                                        dict_pd["file_html"].append(lab_code_info.file_html)
                                if "test_me_inf" not in dict_pd:
                                        dict_pd["test_me_inf"] = [str(test_me)+str(instance)]
                                else:
                                        dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                                if "code_str" not in dict_pd:
                                        dict_pd['code_str'] = [lab_code_info.get_code_str()]
                                else:
                                        dict_pd['code_str'].append(lab_code_info.get_code_str())

                                if 'perf_change' not in dict_pd:
                                        dict_pd['perf_change'] = [instance_feature['perf_change'][0]]
                                else:
                                        dict_pd['perf_change'].append(instance_feature['perf_change'][0])
                                if 'perf_change_left' not in dict_pd:
                                        dict_pd['perf_change_left'] = [instance_feature['perf_change'][1]]
                                else:
                                        dict_pd['perf_change_left'].append(instance_feature['perf_change'][1])
                                if 'perf_change_right' not in dict_pd:
                                        dict_pd['perf_change_right'] = [instance_feature['perf_change'][2]]
                                else:
                                        dict_pd['perf_change_right'].append(instance_feature['perf_change'][2])

                                if "size_obj" not in dict_pd:
                                        dict_pd["size_obj"] = [int(size_obj_dict[test_me][instance][0])]
                                else:
                                        dict_pd["size_obj"].append(int(size_obj_dict[test_me][instance][0]))
                                if "num_ele" not in dict_pd:
                                        dict_pd["num_ele"] = [instance_feature['num_ele']]
                                else:
                                        dict_pd["num_ele"].append(instance_feature['num_ele'])
                                one_code_num_list.append([instance_feature['num_ele'],int(size_obj_dict[test_me][instance][0]),instance_feature['perf_change'][0]])

                                for fea in dict_features:
                                        ele = dict_features[fea]  # np.log(dict_features[fea])
                                        if fea not in dict_pd:
                                                dict_pd[fea] = [ele]
                                        else:
                                                dict_pd[fea].append(ele)
                                count_instance+=1
                count_code+=1
                print("one_code_num_list: ",one_code_num_list,count_size_of_null)

        dataMain = pd.DataFrame(data=dict_pd)
        dataMain = drop_rows_same(dataMain)
        # print(dataMain.to_dict())
        util.save_pkl(feature_info_dir, feature_file_name, dataMain.to_dict())
        dataMain.to_csv(csv_feature_file_name, index=False)
        print("count: ",count_code,count_test_me,count_instance)
def drop_rows_same(df):
        same_feature_list = []
        for index, row in df.iterrows():
                if row['file_html'] + row['code_str'] + str(row['num_ele']) in same_feature_list:
                        df.drop(index, inplace=True)
                else:
                        same_feature_list.append(row['file_html'] + row['code_str'] + str(row['num_ele']))
        return df
def remove_features():
        dict_pd = util.load_pkl(feature_info_dir, feature_file_name)

        # dict_pd["perf_change"] = np.log(dict_pd["perf_change"])
        stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
        # warnings.filterwarnings(action='once')
        warnings.filterwarnings(action='default')
        # load Data
        dataMain = pd.DataFrame(data=dict_pd)
        # print(dataMain.to_dict())
        # dataMain.to_csv(csv_feature_file_name, index=False)


        same_feature_list = []
        for key in dataMain:
                if len(set(dataMain[key])) <= 1:
                        # print(key)
                        same_feature_list.append(key)
                        # dataMain.drop
        print("same_feature_list: ", same_feature_list)
        dataMain.drop(columns=same_feature_list,inplace=True)
        print("all columns: ",dataMain.columns)

        remove_feature_list =["size_obj","num_param","num_Delimiters","num_Keywords",
                              "perf_change_left","perf_change_right",
                              "file_html","test_me_inf","code_str"]#['num_Delimiters','num_var','num_param','num_ele']
        dataMain.drop(columns=remove_feature_list, inplace=True)
        print("all columns without same value in one column: ",dataMain.columns)
        dataMain.to_csv(csv_feature_file_name_corr, index=False)
        '''
        remove_feature_list = ["num_Delimiters_diff", "num_line_diff", "num_Delimiters", 'num_var', 'num_line',
                               "num_var_diff", "num_param_diff", "num_if_else_diff", "num_func_call_diff",
                               "num_func_call", "num_constant", "num_Keywords_diff", 'num_Attr_diff',
                               'num_param', 'num_Operators', "num_Attr", 'num_loop_diff', 'num_if_diff']  # []
        '''
        # feature_important=["num_Delimiters_diff",]
        dict_corr_num = dict()
        corr = dataMain.corr().to_dict()
        print(">>>>>>>>>>>corr:\n ",corr)
        for f1_name in corr:
                for e_another in corr[f1_name]:
                        if corr[f1_name][e_another] is pd.NA or corr[f1_name][e_another] > 0.7 or corr[f1_name][
                                e_another] < -0.7:

                                if f1_name in remove_feature_list or e_another in remove_feature_list:
                                        continue
                                if f1_name not in dict_corr_num:
                                        dict_corr_num[f1_name] = 0
                                dict_corr_num[f1_name] += 1
                                print(f1_name, e_another, corr[f1_name][e_another])
        remove_feature_list = ["num_func_call", "num_Attr", "num_param", "num_var", "num_loop_diff", "num_if_diff"]
        print("dict_corr_num: ", sorted(dict_corr_num.items(), key=lambda kv: (kv[1], kv[0])),len(dataMain))
        # dict_corr_num:  [('num_Keywords', 1), ('num_ele', 1), ('num_if', 1), ('num_if_else', 1), ('num_loop', 1), ('perf_change', 1)]
def all_data_save():
        feature = pd.read_csv(csv_feature_file_name_corr)
        key_list=feature.columns.tolist()
        # print(key_list)
        dict_pd=dict()
        for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
                # break
                print("file_name: ", ind,file_name)
                file_name_no_suffix = file_name[:-4]
                size_obj_dict = util.load_pkl(sizeof_code_info_dir, file_name_no_suffix)
                # print("size_obj_dict: ",size_obj_dict)
                # break
                lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
                lab_code_info: CodeInfo
                for_node, assign_node, remove_ass_flag, new_tree = lab_code_info.code_info
                total_time_list_info_dict = lab_code_info.total_time_list_info_dict
                if not total_time_list_info_dict:
                        continue
                new_node_list = [new_tree]
                if not remove_ass_flag:
                        new_node_list.append(assign_node)
                dict_features = util_perf.get_features([for_node, assign_node])  # .get_features()

                # print("features: ", ast.unparse(for_node), "\n", ast.unparse(assign_node))
                # print("features: ", dict_features)
                one_code_num_list=[]
                for test_me in total_time_list_info_dict:
                        for instance in total_time_list_info_dict[test_me]:
                                instance_feature=total_time_list_info_dict[test_me][instance]
                                if test_me not in size_obj_dict or instance not in size_obj_dict[test_me]:
                                        continue
                                if "file_html" not in dict_pd:
                                        dict_pd["file_html"] = [lab_code_info.file_html]
                                else:
                                        dict_pd["file_html"].append(lab_code_info.file_html)
                                if "test_me_inf" not in dict_pd:
                                        dict_pd["test_me_inf"] = [str(test_me)+str(instance)]
                                else:
                                        dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                                if "size_obj" not in dict_pd:
                                        dict_pd["size_obj"] = [int(size_obj_dict[test_me][instance][0])]
                                else:
                                        dict_pd["size_obj"].append(int(size_obj_dict[test_me][instance][0]))
                                if "num_ele" not in dict_pd:
                                        dict_pd["num_ele"] = [instance_feature['num_ele']]
                                else:
                                        dict_pd["num_ele"].append(instance_feature['num_ele'])
                                one_code_num_list.append([instance_feature['num_ele'],int(size_obj_dict[test_me][instance][0]),instance_feature['perf_change'][0]])

                                if 'perf_change' not in dict_pd:
                                        dict_pd['perf_change'] = [instance_feature['perf_change']]#instance_feature['perf_change'][0]
                                else:
                                        dict_pd['perf_change'].append(instance_feature['perf_change'])#instance_feature['perf_change'][0]
                                for fea in dict_features:
                                        if fea not in key_list:
                                                continue
                                        ele = dict_features[fea]  # np.log(dict_features[fea])
                                        if fea not in dict_pd:

                                                dict_pd[fea] = [ele]
                                        else:
                                                dict_pd[fea].append(ele)

        dataMain = pd.DataFrame(data=dict_pd)
        # print(dataMain.to_dict())
        dataMain.to_csv("all_feature_list_comprehension.csv", index=False)




if __name__ == '__main__':

        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks/final_stable/"
        bench_time_info_dir = util.data_root + "lab_performance/list_compre_benchmarks_mod/prefined_cpus_remain_code/"
        bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_perf_change/"
        feature_info_dir=util.data_root + "lab_performance/feature/list_compre_benchmarks/"
        feature_file_name="list_comprehension"
        feature_file_name="list_comprehension_original"
        feature_file_name="list_comprehension_original_complete_features"
        feature_file_name="list_compre_benchmarks_complete_features"
        feature_file_name="list_compre_benchmarks_complete_features_add_sizeof"
        feature_file_name="list_compre_benchmarks_complete_features_add_sizeof_correct_perf_change"
        feature_file_name="list_compre_benchmarks_complete_features_add_sizeof_correct_perf_change_callNoAppend"
        csv_feature_file_name="labperformance_listcomprehension_complete_feature.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change_callNoAppend.csv"
        csv_feature_file_name="performance_listcomprehension_complete_feature_add_sizeof_correct_perf_change_callNoAppend_no_same_feature_vector.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_corr.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend.csv"
        csv_feature_file_name_corr="performance_listcomprehension_complete_feature_add_sizeof_corr_correct_perf_change_callNoAppend_no_same_feature_vector.csv"
        #'''
        sizeof_code_info_dir = util.data_root + "performance/list_compre_benchmarks_sizeof_feature/"
        dynamic_code_info_dir = util.data_root + "performance/list_compre_benchmarks_sizeof_type_num_ele_feature/"

        get_data_type()


import time

import numpy as np, scipy.stats as st
import sys,ast,os,csv,time,copy

import subprocess

import scipy.stats

code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"wrap_refactoring/")
import refactor_list_comprehension
import performance_replace_content_by_ast_time_percounter
import lab_performance_util
import util
from lab_code_info import LabCodeInfo


def dynamic_determine_confiden_interval(time_list, warmups=0):
    all_mea_time_list = []

    result, mean, invo = None, None, len(time_list)
    if isinstance(time_list, list):

        for ind_inv, inv_list in enumerate(time_list):
            # print(">>>>>>>>>>: ", ind_inv)
            mea_time_list = copy.deepcopy(inv_list[warmups:])
            all_mea_time_list.append(mea_time_list)
            if len(all_mea_time_list) > 2:
                mean_list = []
                new_all_mea_time_list = lab_performance_util.num_bootstrap(all_mea_time_list, 1000)
                # print(new_all_mea_time_list[:5])
                for e in new_all_mea_time_list:
                    mean_list.append(np.mean(e, dtype=np.float32))

                # new_all_mea_time_list = copy.deepcopy(all_mea_time_list)
                # for i in range(1000):
                #     lab_performance_util.bootstrap(all_mea_time_list, new_all_mea_time_list)
                #     # print(np.array(new_all_mea_time_list).shape)
                #     mean_list.append(np.mean(new_all_mea_time_list, dtype=np.float32))
                # print("mean: ",np.mean(all_mea_time_list, dtype=np.float32),np.mean(mean_list, dtype=np.float32))
                left, right = np.percentile(mean_list, [2.5, 97.5])
                # print("percentile:",np.percentile(mean_list, [2.5, 97.5]))
                # result = st.t.interval(0.95, len(mean_list) - 1, loc=np.mean(mean_list), scale=st.sem(mean_list))
                mean = np.mean(all_mea_time_list, dtype=np.float32)
                # print("left / mean, right/mean:", left / mean,right/mean)
                if left / mean >= 0.97 and right / mean <= 1.03:
                    print(">>>>>come here: ", ind_inv)
                    invo = ind_inv + 1
                    # print(result, np.mean(mean_list), result[0] / np.mean(mean_list),
                    #       result[1] / np.mean(mean_list),
                    #       np.mean(mean_list) - result[0], np.mean(mean_list) - result[1])
                    return left, right, mean, invo
    else:
        pass

    return None
def determine_time_list_stable(time_list,idiom_time_list,warmups=0):
    mean_list = []
    idiom_mean_list = []

    all_idiom_mea_time_list = []

    idiom_rciw = dynamic_determine_confiden_interval(idiom_time_list,warmups)
    rciw = dynamic_determine_confiden_interval(time_list,warmups)
    # idiom_rciw = dynamic_determine_confiden_interval([sum(e[4:]) for e in idiom_time_list])
    # rciw = dynamic_determine_confiden_interval([sum(e[4:]) for e in time_list])
    if rciw:
        # print('yes')
        pass
    else:
        print("no rciw")
        print(time_list)
        print(idiom_time_list)

    if not idiom_rciw:
        print("no idiom_rciw")
        print(idiom_time_list)
'''

'''
if __name__ == '__main__':
    # bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/code_time_info_prefined_cpu/"
    # bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/code_time_info_improve/"
    # bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/code_time_info/"
    bench_time_info_dir=util.data_root + "lab_performance/list_compre_benchmarks/code_time_info_improve/"
    bench_dir = util.data_root + "lab_performance/list_compre_benchmarks/code/code/"#code/
    print("all code: ",len(os.listdir(bench_dir)))
    data=[]
    print("len: ",len(os.listdir(bench_time_info_dir)))
    for ind,file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
        # if ind>10:
        #     break
        # if file_name!="2_4_3_[1].pkl":#"1_1_0_list(range(1,11))*10.pkl":#
        #     continue
        # print("file_name: ",file_name)
        file_name_no_suffix=file_name[:-4]
        lab_code_info=util.load_pkl(bench_time_info_dir,file_name_no_suffix)
        lab_code_info:LabCodeInfo
        # print("code path: ",lab_code_info.file_path)
        invocations,iterations,num_add_ele=lab_code_info.invocations,lab_code_info.iterations,lab_code_info.num_add_ele
        num_for,num_if,num_if_else,e_input=file_name_no_suffix.split("_")

        time_list=lab_code_info.compli_code_time_dict
        idiom_time_list=lab_code_info.simple_code_time_dict
        time_list = [[float(e)  for e in e_list] for e_list in time_list]
        idiom_time_list =[[float(e)  for e in e_list]for e_list in idiom_time_list]

        time_list=lab_performance_util.filter_warms(time_list,3)
        idiom_time_list = lab_performance_util.filter_warms(idiom_time_list, 3)
        mad=st.median_abs_deviation(time_list,None, scale=1)
        idiom_mad = st.median_abs_deviation(idiom_time_list,None, scale=1)
        '''
        print(st.median_abs_deviation([1,2,3,4,5],scale=1))
        print("mad, median: ",mad,np.median(real_time_list))
        print("idiom mad, median: ", idiom_mad, np.median(real_idiom_time_list))
        print(st.median_abs_deviation(real_idiom_time_list))
        '''
        # time_list=lab_performance_util.filter_outliners(time_list,np.median(time_list),3*mad)
        # idiom_time_list=lab_performance_util.filter_outliners(idiom_time_list,np.median(idiom_time_list),3*mad)

        all_time_list = lab_performance_util.num_bootstrap(time_list, 1000)
        all_idiom_time_list = lab_performance_util.num_bootstrap(idiom_time_list, 1000)
        per_change_list=[]
        for ind,e_time_list in enumerate(all_time_list):
            e_idiom_time_list=all_idiom_time_list[ind]
            e_sum=sum([sum(e) for e in e_time_list])
            e_idiom_sum=sum([sum(e) for e in e_idiom_time_list])
            # print("e_time_list: ",sum(e_time_list))
            # print(e_idiom_time_list)
            # print(np.mean(np.array(e_time_list,dtype=np.float64),None))
            per_change=e_sum/e_idiom_sum
            per_change_list.append(per_change)
        left, right = np.percentile(per_change_list, [2.5, 97.5])
        if left<1<right:
            print("file_name: ", file_name)
            e_sum = sum([sum(e) for e in time_list])
            e_idiom_sum = sum([sum(e) for e in idiom_time_list])
            print(left, right, e_sum/e_idiom_sum)
        else:
            # print("file_name: ", file_name)
            # e_sum = sum([sum(e) for e in time_list])
            # e_idiom_sum = sum([sum(e) for e in idiom_time_list])
            # print(left, right, e_sum / e_idiom_sum)
            pass


        '''
        all_new_list=lab_performance_util.num_bootstrap(time_list[:rciw[-1]])
        all_idiom_new_list=lab_performance_util.num_bootstrap(idiom_time_list[:idiom_rciw[-1]])
        
        print("len: ",len(all_new_list))
        performance_change_list=[]
        for i,e in enumerate(all_new_list):
            mean_old=e
            mean_new=all_idiom_new_list[i]
            # print(np.mean(mean_old,dtype=np.float32),np.mean(mean_new,dtype=np.float32))
            pr=np.mean(mean_old,dtype=np.float32)/np.mean(mean_new,dtype=np.float32)
            performance_change_list.append(pr)
            # break
        mean_pr=np.mean(performance_change_list)
        result = st.t.interval(0.95, len(performance_change_list) - 1, loc=np.mean(performance_change_list), scale=st.sem(performance_change_list))
        print(result,mean_pr)
        '''


        # for ind_inv,inv_list in enumerate(time_list):
        #     mea_time_list=copy.deepcopy(inv_list[3:])
        #     idiom_mea_time_list=copy.deepcopy(idiom_time_list[ind_inv][3:])
        #     all_mea_time_list.append(mea_time_list)
        #     all_idiom_mea_time_list.append(idiom_mea_time_list)
        #     if len(all_mea_time_list)>2:
        #         new_all_mea_time_list=copy.deepcopy(all_mea_time_list)
        #         for i in range(1000):
        #             lab_performance_util.bootstrap(all_mea_time_list, new_all_mea_time_list)
        #             # print(np.array(new_all_mea_time_list).shape)
        #             mean_list.append(np.mean(new_all_mea_time_list,dtype=np.float32))
        #         import numpy as np, scipy.stats as st
        #         result=st.t.interval(0.95, len(mean_list) - 1, loc=np.mean(mean_list), scale=st.sem(mean_list))
        #         if result[0]/np.mean(mean_list)>=0.97:
        #             print(result, np.mean(mean_list), result[0] / np.mean(mean_list), result[1] / np.mean(mean_list),
        #                   np.mean(mean_list) - result[0], np.mean(mean_list) - result[1])
        #
        #             break
                # print(result,np.mean(mean_list),result[0]/np.mean(mean_list),result[1]/np.mean(mean_list),np.mean(mean_list)-result[0],np.mean(mean_list)-result[1])
                # break
            # for ind_iter, iter_time in enumerate(inv_list):

        # break



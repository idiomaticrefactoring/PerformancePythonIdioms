import sys, ast, os, csv, time, copy
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
print("code_dir: ",code_dir)
sys.path.append(code_dir+"performance/")
# from code_info import CodeInfo
# from code_info import CodeInfo
import util, performance_util

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    save_code_info_dir_add_performance_change = \
        util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_2nd_invo_step_100/50/"
    # save_code_info_dir_add_performance_change = \
    #     util.data_root + "performance/tosem_2020_list_compre_bench_rq_1_1st_invo_step_100/50/"

    dict_pd = {
            "file_html": [], "test_me_inf":[], "instance":[],"code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []

        }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        # lab_code_info
        file_html = lab_code_info.file_html
        if file_html!="https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/transforms/repconversions/qubit_tapering_from_stabilizer.py":
            continue
        code_str = lab_code_info.get_code_str()
        perf_info_dict = lab_code_info.total_time_list_info_dict
        # print("file_name: ", file_name, perf_info_dict)
        # if 1:
        for test_me in perf_info_dict:
            for instance in perf_info_dict[test_me]:
                perf_info = perf_info_dict[test_me][instance]["perf_change"]
                if instance!=8:
                    continue
                print("perf_info: ", file_name, test_me,instance,perf_info)
                dict_pd["file_html"].append(file_html)
                dict_pd["test_me_inf"].append(str(test_me))
                dict_pd["instance"].append(str(instance))

                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["RCIW"].append((perf_info[2]-perf_info[1])/perf_info[0])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])

import sys,ast,os,csv,time,copy,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
import util,lab_performance_util
from lab_code_info import LabCodeInfo
import pandas as pd

def save_features_add_interval(bench_time_info_dir):
    dict_pd = {"perf_change":[],"num_assign_node":[],"type_data_input":[],"context":[],"swap_flag":[]}

    # '''
    for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
        print("file_name: ", file_name)
        num_node_str=int(file_name.split("_")[0])
        if "_swap" in file_name:
            dict_pd["swap_flag"].append("swap")
        else:
            dict_pd["swap_flag"].append("Nswap")
        dict_pd["num_assign_node"].append(num_node_str)

        if "_const" in file_name:
            dict_pd["type_data_input"].append("const")

        else:
            dict_pd["type_data_input"].append("Nconst")
            # break
        if "_func" in file_name:
            dict_pd["context"].append("func")
        else:
            dict_pd["context"].append("Nfunc")

        '''
        if "_swap" in file_name:
            dict_pd["swap_flag"].append("1")
        else:
            dict_pd["swap_flag"].append("0")
        dict_pd["num_assign_node"].append(num_node_str)
        
        if "_const" in file_name:
            dict_pd["type_data_input"].append("1")

        else:
            dict_pd["type_data_input"].append("0")
            # break
        if "_func" in file_name:
            dict_pd["context"].append("1")
        else:
            dict_pd["context"].append("0")
        '''
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        dict_pd["perf_change"].append(lab_code_info.perf_ci_info[0])
        # print(dict_pd)
        # break


    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)


if __name__ == '__main__':
    # bench_time_info_dir = \
    #     util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    #
    bench_time_info_dir=util.data_root + "lab_performance/multi_ass_benchmarks/bench_time_info_dir_prefined_cpu_new/"
    bench_time_info_dir = \
        util.data_root + "lab_performance/multi_ass_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/50/"

    csv_feature_file_name_corr=util.data_root + "lab_performance/multi_ass_benchmarks/csv/multi_ass_feature.csv"
    save_features_add_interval(bench_time_info_dir)
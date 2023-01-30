import sys,ast,os,csv,time,copy,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
import util,lab_performance_util
from lab_code_info import LabCodeInfo
import pandas as pd

def save_features_add_interval(bench_time_info_dir):
    dict_pd = {"perf_change":[],"node_test":[],"node_cmpop":[],"data_input":[],"context":[]}

    # '''
    for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
        print("file_name: ", file_name)
        data_str=file_name.split("_")[0]
        dict_pd["data_input"].append(data_str)
        if "==" in file_name:
            dict_pd["node_cmpop"].append("==")
        else:
            dict_pd["node_cmpop"].append("!=")
        if "if" in file_name:
            dict_pd["node_test"].append("if")
        elif "while" in file_name:
            dict_pd["node_test"].append("while")
        else:
            dict_pd["node_test"].append("assert")
            # break
        if "_func" in file_name:
            dict_pd["context"].append("func")
        else:
            dict_pd["context"].append("Nfunc")

        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        dict_pd["perf_change"].append(lab_code_info.perf_ci_info[0])
        # print(dict_pd)
        # break


    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)


if __name__ == '__main__':
    bench_time_info_dir = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    csv_feature_file_name_corr= util.data_root_mv + "lab_performance/truth_value_test_benchmarks/csv/truth_value_test_feature.csv"
    save_features_add_interval(bench_time_info_dir)
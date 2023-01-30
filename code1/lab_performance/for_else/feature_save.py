import sys,ast,os,csv,time,copy,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
import util,lab_performance_util
from lab_code_info import LabCodeInfo
import pandas as pd

def save_features_add_interval(bench_time_info_dir):
    dict_pd = {"file_html": [], "code_str": [], 'perf_change': [],
               "node_kind":[],"branch_through_break":[],"data_input_size":[],"context":[],"has_else":[]
               , 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []}

    # '''
    for ind, file_name in enumerate(os.listdir(bench_time_info_dir)[:]):
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        file_html = lab_code_info.file_path
        code_str = lab_code_info.get_code_str()
        perf_info_dict = lab_code_info.perf_ci_info
        perf_info = perf_info_dict
        dict_pd["file_html"].append(file_html)
        dict_pd["code_str"].append(code_str)

        dict_pd["perf_change"].append(perf_info[0])
        dict_pd["RCIW"].append(perf_info[3])
        dict_pd["perf_change_left"].append(perf_info[1])
        dict_pd["perf_change_right"].append(perf_info[2])
        print("file_name: ", file_name)
        data_str=file_name.split("_")[0]
        dict_pd["data_input_size"].append(int(data_str))
        if "for" in file_name:
            dict_pd["node_kind"].append("for")
        else:
            dict_pd["node_kind"].append("while")
        if "1_break" in file_name:
            dict_pd["branch_through_break"].append("break")

        else:
            dict_pd["branch_through_break"].append("Nbreak")
            # break
        if "_func" in file_name:
            dict_pd["context"].append("func")
        else:
            dict_pd["context"].append("Nfunc")


        if "1_else" in file_name:
            dict_pd["has_else"].append("else")
        else:
            dict_pd["has_else"].append("Nelse")

        # file_name_no_suffix = file_name[:-4]
        # lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        # lab_code_info: LabCodeInfo
        # dict_pd["perf_change"].append(lab_code_info.perf_ci_info[0])
        # print(dict_pd)
        # break


    dataMain = pd.DataFrame(data=dict_pd)
    dataMain.to_csv(csv_feature_file_name_corr, index=False)


if __name__ == '__main__':
    bench_time_info_dir = \
        util.data_root_mv + "lab_performance/truth_value_test_benchmarks/prefined_cpus_remain_code_new_add_perf_change_remove_oulier_factor_3/"
    bench_time_info_dir = \
        util.data_root_mv + "lab_performance/for_else_benchmarks/prefined_cpus_remain_code_new_add_perf_change/"

    csv_feature_file_name_corr= util.data_root_mv + "lab_performance/for_else_benchmarks/csv/for_else_feature.csv"
    save_features_add_interval(bench_time_info_dir)
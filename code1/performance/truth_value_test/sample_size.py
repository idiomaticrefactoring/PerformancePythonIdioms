import random
import sys, ast, os, csv, time, traceback

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-3]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + "performance/")
import util,performance_util
if __name__ == '__main__':
    list = [i for i in range(10)]
    n=1
    random.seed(2022)
    samples = random.sample(list, n)
    print("samples: ",samples)
    file_dir=util.data_root+"format_code_info/"
    file_name="truth_value_test_complete"#"chain_compare_complete"
    code_time_list=[]
    pro_path = util.data_root + "python_star_2000repo/"
    code_info_list = util.load_pkl(file_dir, file_name)
    list = [i for i in range(len(code_info_list))]
    n = 330
    random.seed(2022)
    samples = random.sample(list, n)
    print("samples: ",len(samples))
    sample_code_list=[]
    for e in sorted(samples):
        sample_code_list.append(code_info_list[e])
    util.save_pkl(util.data_root + "format_code_info/", "truth_value_test_sample_330", sample_code_list)

    remain_list=set(list)-set(samples)
    random.seed(2022)
    samples = random.sample(remain_list, len(remain_list))
    print("samples: ", samples)
    print("samples: ", len(samples))
    sample_code_list = []
    for e in sorted(samples):
        sample_code_list.append(code_info_list[e])
    util.save_pkl(util.data_root + "format_code_info/", "truth_value_test_sample_remain_all", sample_code_list)
    print(len(code_info_list))
        # add_samples_110=[]
    # util.save_pkl(util.data_root + "format_code_info/", "multi_ass_sample_317_2021", sample_code_list)
    # util.save_pkl(util.data_root + "format_code_info/", "multi_ass_sample_317_20", sample_code_list)

    # util.data_root + "format_code_info/", "multi_ass_complete"
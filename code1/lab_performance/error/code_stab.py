import time
import numpy as np
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"wrap_refactoring/")
import lab_performance_util
import util
from lab_code_info import LabCodeInfo

# log_time_info_dir = util.code_root + "lab_performance/error/log/"
log_time_info_dir = util.code_root + "lab_performance/error/log_two_time_add/"

all_mea_time_list=[]
for ind,file_name in enumerate(os.listdir(log_time_info_dir)):

    output=util.load_file_path(log_time_info_dir+file_name)
    get_time_list = lab_performance_util.get_time_list(output)
    get_time_list=[ float(e) for e in get_time_list]
    print(get_time_list)
    # continue
    all_mea_time_list.append(get_time_list)
    if ind<2:
        continue
    new_all_mea_time_list = lab_performance_util.num_bootstrap(all_mea_time_list, 1000)
    # print(new_all_mea_time_list[:5])
    mean_list=[]
    for e in new_all_mea_time_list:
        mean_list.append(np.mean(e, dtype=np.float32))

    print("mean: ", np.mean(all_mea_time_list, dtype=np.float32), np.mean(mean_list, dtype=np.float32))
    left, right = np.percentile(mean_list, [2.5, 97.5])
    print("percentile:", np.percentile(mean_list, [2.5, 97.5]))
    # result = st.t.interval(0.95, len(mean_list) - 1, loc=np.mean(mean_list), scale=st.sem(mean_list))
    mean = np.mean(all_mea_time_list, dtype=np.float32)
    print("left / mean, right/mean:", left / mean, right / mean)
    if left / mean >= 0.97 and right / mean <= 1.03:
        print("come here",ind)
        break

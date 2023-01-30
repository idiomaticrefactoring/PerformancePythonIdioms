import time
import numpy as np
import sys,ast,os,csv,time,copy
import subprocess
import pandas as pd
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"test_case/")
import util
from lab_code_info import LabCodeInfo
import configure_pro_envir_util
import random
def save_perf_change(file_name,bench_time_info_dir,save_code_info_dir_add_performance_change,invo=50):

    file_name_no_suffix = file_name[:-4]
    lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
    lab_code_info: LabCodeInfo

    # print("total_time_list_info_dict: ",total_time_list_info_dict)
    # for invo in invo_list:
    lab_code_info.get_performance_improve_info()
    print("performance change: ",lab_code_info.perf_ci_info)
    util.save_pkl(save_code_info_dir_add_performance_change + str(invo) + "/", file_name_no_suffix, lab_code_info)
    print("save ",save_code_info_dir_add_performance_change + str(invo) + "/", file_name_no_suffix, "successfully")
    pass
def get_ci_perf_change_dict(save_code_info_dir_add_performance_change,filter_flag=0,file_name_list=[]):
    dict_pd = {
        "file_html": [], "code_str": [], 'perf_change': [], 'RCIW': [], 'perf_change_left': [], 'perf_change_right': []

    }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        if filter_flag:
            if file_name not in file_name_list:
                continue
        print("file_name: ", file_name)
        file_name_no_suffix = file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        file_html = lab_code_info.file_path
        code_str = lab_code_info.get_code_str()
        perf_info_dict = lab_code_info.perf_ci_info
        print("file_name: ", file_name, perf_info_dict)
        if 1:
            # for test_me in perf_info_dict:
            #     for instance in perf_info_dict[test_me]:
            perf_info = perf_info_dict
            dict_pd["file_html"].append(file_html)
            # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
            dict_pd["code_str"].append(code_str)

            dict_pd["perf_change"].append(perf_info[0])
            dict_pd["RCIW"].append(perf_info[3])
            dict_pd["perf_change_left"].append(perf_info[1])
            dict_pd["perf_change_right"].append(perf_info[2])
    return dict_pd
def save_csv_perf_change(save_code_info_dir_add_performance_change,csv_perf_change_dir,csv_file_name="csv_perf_change_result.csv"):
    dict_pd={
        "file_html":[],"code_str":[],'perf_change':[],'RCIW':[],'perf_change_left':[],'perf_change_right':[]

    }
    print("************perf csv save******************")
    for file_name in sorted(os.listdir(save_code_info_dir_add_performance_change)):
        file_name_no_suffix=file_name[:-4]
        lab_code_info = util.load_pkl(save_code_info_dir_add_performance_change, file_name_no_suffix)
        lab_code_info: LabCodeInfo
        file_html=lab_code_info.file_path
        code_str=lab_code_info.get_code_str()
        perf_info_dict=lab_code_info.perf_ci_info
        print("file_name: ",file_name,perf_info_dict)
        if 1:
        # for test_me in perf_info_dict:
        #     for instance in perf_info_dict[test_me]:
                perf_info=perf_info_dict
                dict_pd["file_html"].append(file_html)
                # dict_pd["test_me_inf"].append(str(test_me)+str(instance))
                dict_pd["code_str"].append(code_str)

                dict_pd["perf_change"].append(perf_info[0])
                dict_pd["RCIW"].append(perf_info[3])
                dict_pd["perf_change_left"].append(perf_info[1])
                dict_pd["perf_change_right"].append(perf_info[2])

    dataMain = pd.DataFrame(data=dict_pd)
    # print(">>>>>>drop same features: ", dataMain.keys())
        # print(dataMain.to_dict())
    dataMain.to_csv(csv_perf_change_dir+csv_file_name, index=False)
def filter_warms(time_list,warmups=1):
    new_time_list=[]
    for e in time_list:
        new_time_list.append(e[warmups:])
    return new_time_list
def filter_outliners(time_list,base,interval):
    new_time_list=[]
    for e_list in time_list:
        new_e_list=[]
        for e in e_list:
            if interval >=e-base>=-interval:
                new_e_list.append(e)
        else:
            # print("outliners:",e,base)
            pass
        if new_e_list:
            new_time_list.append(new_e_list)
    return new_time_list


def bootstrap(x,x_new):
    if isinstance(x, list):
        new_index=random.choices([i for i in range(len(x))],k=len(x))
        # print("new_index: ",new_index)
        for i,e in enumerate(x):
                x_new[i]=copy.deepcopy(x[new_index[i]])
                # print(x_new)
                bootstrap(x[new_index[i]],x_new[i])
def num_bootstrap(x,steps=1000):
    all_x_new=[]

    for i in range(steps):
        x_new = copy.deepcopy(x)
        bootstrap(x, x_new)
        all_x_new.append(x_new)
    return all_x_new
def whether_cov(time_list,window):

    for i in range(len(time_list) - window + 1):
            cov = np.std(time_list[i:i + window]) / np.mean(time_list[i:i + window])
            if cov <= 0.02:
                return 1
    return 0


def whether_all_invocations_stable(valid_time_list, file_name):
    mean_time_list = [np.mean(e) for e in valid_time_list]

    mean_time = np.mean(mean_time_list)
    interval, interval_ratio = get_interval_t_dis(mean_time_list)
    if interval_ratio > 0.03:
        # file_unstable_count+=1
        print(f"the interval of {file_name} file is larger 0.03: ", mean_time, interval, interval_ratio)
        return 0
    return 1
def get_time_list_within_cov(time_list,window):
    valid_time_list = []
    for ind_t, e in enumerate(time_list):
        for i in range(len(e) - window + 1):
            cov = np.std(e[i:i + window]) / np.mean(e[i:i + window])
            if cov <= 0.02:
                valid_time_list.append(e[i:i + window])
                break
    return valid_time_list
def get_time_list_within_cov_contain_index(time_list,window):
    valid_time_list = []
    index_list=[]
    for ind_t, e in enumerate(time_list):
        for i in range(len(e) - window + 1):
            cov = np.std(e[i:i + window]) / np.mean(e[i:i + window])
            if cov <= 0.02:
                index_list.append(i)
                valid_time_list.append(e[i:i + window])
                break
    return valid_time_list,index_list
def whether_time_list_within_cov(time_list,window):
    for ind_t, e in enumerate(time_list):
        for i in range(len(e) - window + 1):
            cov = np.std(e[i:i + window]) / np.mean(e[i:i + window])
            if cov <= 0.02:
                break
        else:
            return 0

    return 1
def whether_time_list_within_cov_for_given_number(time_list,window,number=10):
    stable_count=0
    for ind_t, e in enumerate(time_list):
        for i in range(len(e) - window + 1):
            cov = np.std(e[i:i + window]) / np.mean(e[i:i + window])
            if cov <= 0.02:
                stable_count+=1
                if stable_count >= number:
                    return 0
                break


    return 1
'''
def get_interval_t_dis(mean_time_list,alpha=0.95):
    mean_time = np.mean(mean_time_list)
    # https://vedexcel.com/how-to-calculate-confidence-intervals-in-python/
    interval = st.t.interval(alpha=alpha, df=len(mean_time_list) - 1, loc=np.mean(mean_time_list),
                             scale=st.sem(mean_time_list))
    interval_ratio = (interval[1] - mean_time) / mean_time
    return interval,interval_ratio
'''
def get_time_list(run_test_result_new):
    time_list=[]
    ind=len("*********zejun test total time**************")
    for e in run_test_result_new.split("\n"):
        if e.startswith("*********zejun test total time**************"):
            time_list.append(e[ind:].strip())
    return time_list
def get_pythonic_time_list(run_test_result_new):
    time_list=[]
    ind=len("*********zejun test total time pythonic**************")
    for e in run_test_result_new.split("\n"):
        if e.startswith("*********zejun test total time pythonic**************"):
            time_list.append(e[ind:].strip())
    return time_list
def sequence_run_by_dir(code_dir,python_version='7',invocations=1,log_dir=""):
    os.chdir(code_dir)
    for invo in range(invocations):
        for file_name in os.listdir(code_dir):
            if '.py' not in file_name:
                continue

            cmd_virtu = configure_pro_envir_util.create_virtual_envi(code_dir, 'ven', python_version)
            log_path = log_dir+file_name[:-3] + '_' + str(invo) + '.log'
            python_cmd = "".join(
                ['nohup python3', "  '", file_name, "' > '", log_path,
                 "'  2>&1"])
            total_cmd = "".join([cmd_virtu,python_cmd,";cat '",log_path,"';   deactivate"])#, ";deactivate"
            result = subprocess.run(total_cmd, shell=True, timeout=15 * 60, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            print("result: ",result)
            while True:
                if os.path.exists(log_path):
                    with open(log_path, "r") as f:
                        if 'code is finished' in f.read():
                            break
            time.sleep(10)

def sequence_run(code_dir,file_name,python_version='7',invo=1,log_dir="",prefined_cpu=""):
            start_time=time.time()
            os.chdir(code_dir)

    # for invo in range(invocations):
        # for file_name in os.listdir(code_dir):
        #     if '.py' not in file_name:
        #         continue
            if os.path.exists(code_dir+"/"+'ven'+python_version):
                cmd_virtu =configure_pro_envir_util.activate_virtual_envi(code_dir, 'ven', python_version)
            else:
                cmd_virtu = configure_pro_envir_util.create_virtual_envi(code_dir, 'ven', python_version)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_path = log_dir+file_name[:-3] + '_' + str(invo) + '.log'
            if os.path.exists(log_path):
                print("remove success: ",log_path)
                os.remove(log_path)
            python_cmd = "".join(
                [prefined_cpu+' nohup python3 ', "  '", file_name, "' > '", log_path,
                 "'  2>&1"])
            total_cmd = "".join([cmd_virtu,python_cmd,";cat '",log_path,"';   deactivate"])#, ";deactivate"
            # print("total_cmd: ",total_cmd)
            result = subprocess.run(total_cmd, shell=True, timeout=15 * 60, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            std_out_res = result.stdout.decode("utf-8")
            # print("std_out_res: \n", result)
            std_error = result.stderr.decode("utf-8") if result.stderr else ""
            std_args = result.args
            # print("\n".join(result.stdout.decode("utf-8").split("*************************test*************************")))

            # print("std_error: \n", std_error)
            # print("std_args: \n", std_args)
            output = "\n".join([std_out_res, std_error, std_args])
            # print("result: ",output)
            while True:

                if os.path.exists(log_path):
                    with open(log_path, "r") as f:
                        if 'code is finished' in f.read():
                            print("run a code is finished")
                            break
                        # else:
                        #     print("log content: ",f.read())
                        if time.time()-start_time>20*60:
                            print("time has reached 20 mins")
                            break
            # time.sleep(1)
            return output


def sequence_run_norm(code_dir, file_name, python_version='7', invo=1, log_dir="", prefined_cpu=""):
    start_time = time.time()
    os.chdir(code_dir)

    # for invo in range(invocations):
    # for file_name in os.listdir(code_dir):
    #     if '.py' not in file_name:
    #         continue
    if os.path.exists(code_dir + "/" + 'ven' + python_version):
        cmd_virtu = configure_pro_envir_util.activate_virtual_envi(code_dir, 'ven', python_version)
    else:
        cmd_virtu = configure_pro_envir_util.create_virtual_envi(code_dir, 'ven', python_version)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_path = log_dir + file_name[:-3] + '_' + str(invo) + '.log'
    if os.path.exists(log_path):
        print("nohup python3.9 get_time_list_compre_improve_system_add_func_Nfunc.py > get_time_list_compre_improve_system_add_func_Nfunc_new_config.log  2>&1 &", log_path)
        os.remove(log_path)
    python_cmd = "".join(
        [prefined_cpu + ' nohup python3 ', file_name, " > ", log_path,
         "  2>&1"])
    total_cmd = "".join([cmd_virtu, python_cmd, ";cat '", log_path, "';   deactivate"])  # , ";deactivate"
    result = subprocess.run(total_cmd, shell=True, timeout=15 * 60, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    std_out_res = result.stdout.decode("utf-8")
    # print("std_out_res: \n", result)
    std_error = result.stderr.decode("utf-8") if result.stderr else ""
    std_args = result.args
    # print("\n".join(result.stdout.decode("utf-8").split("*************************test*************************")))

    # print("std_error: \n", std_error)
    # print("std_args: \n", std_args)
    output = "\n".join([std_out_res, std_error, std_args])
    # print("result: ", output)
    while True:

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                if 'code is finished' in f.read():
                    print("run a code is finished")
                    break
                if time.time() - start_time > 20 * 60:
                    print("time has reached 20 mins")
                    break
    # time.sleep(1)
    return output
def insert_iterations(new_content,iterations):
    all_lines = []
    flag_indent = 0

    for line in new_content.split("\n"):
        if flag_indent:
            line = " " * 4 + line
        all_lines.append(line)
        if line.startswith("import time") or line.startswith("    import time"):

            if line.startswith("import time"):
                all_lines.append(f"for i in range({iterations}):\n")

            elif line.startswith("    import time"):
                all_lines.append(f"    for i in range({iterations}):\n")

            flag_indent = 1
            # break
        elif "zejun test total time" in line:
            flag_indent = 0

    new_add_iterations_content = "\n".join(all_lines)
    return new_add_iterations_content
def insert_iterations_for_else(new_content,iterations):
    all_lines = []
    flag_indent = 0
    flag_inset = 0
    for line in new_content.split("\n"):
        if flag_indent:
            line = " " * 4 + line
        all_lines.append(line)
        if line.startswith("def func_a()") or line.startswith("if __name__ == '__main__':"):
            if flag_inset:
                continue
            if line.startswith("if __name__ == '__main__':"):
                all_lines.append(f"    for i in range({iterations}):\n")
                flag_inset = 1
            elif line.startswith("def func_a()"):
                all_lines.append(f"    for i in range({iterations}):\n")
                flag_inset = 1
            flag_indent = 1
        elif "zejun test total time" in line:
            flag_indent = 0

    new_add_iterations_content = "\n".join(all_lines)
    return new_add_iterations_content
def insert_iterations_truth_value_test(new_content,iterations):
    all_lines = []
    flag_indent = 0
    flag_inset = 0
    for line in new_content.split("\n"):
        if line.startswith("def func_a()") or line.startswith("if __name__ == '__main__':"):
            flag_inset += 1
        if flag_indent and flag_inset<2 and 'code is finished' not in line:
            line = " " * 4 + line
        all_lines.append(line)
        if line.startswith("def func_a()") or line.startswith("if __name__ == '__main__':") and flag_inset<2:
            all_lines.append(f"    for i in range({iterations}):\n")
            flag_indent = 1

        # # if flag_inset>1:
        #     #     flag_indent=0
        #         # continue
        #     if flag_inset==1:
        #         flag_indent = 1
        #     elif not flag_inset:
        #         flag_indent=1
        #     flag_inset += 1
        #     if flag_inset>1:
        #         flag_indent = 0

            # if line.startswith("if __name__ == '__main__':"):
            #     all_lines.append(f"    for i in range({iterations}):\n")
            #     flag_inset += 1
            # elif line.startswith("def func_a()"):
            #     all_lines.append(f"    for i in range({iterations}):\n")
            #     flag_inset = 1
            # # if flag_inset>1:
            # flag_indent = 1
        # elif "zejun test total time" in line:
        #     flag_indent = 0

    new_add_iterations_content = "\n".join(all_lines)
    return new_add_iterations_content
def get_num_add_ele(content):
    for line in content.split("\n"):
        if line.startswith("len: "):
            num=line.split(":")[-1].strip()
            if num.isdigit():
                return str(num)
    return None



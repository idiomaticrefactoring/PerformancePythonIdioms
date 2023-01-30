import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util
func_def_str="def func_a():\n"
if_main_str="\nif __name__ == '__main__':\n    func_a()"
bench_dir=util.data_root_mv + "lab_performance/for_multi_targets_benchmarks_2/code/code/"
input_list_ele_num=7 #
input_unpack_sub_ele_num=5
input_dimen=2
subscript_num=30
flag_need_star=0
count=0
file_name_list=set([])
for i in range(input_list_ele_num):
    # if i!=0:
    #     continue
    for dim_i in range(input_dimen):
        for unpack_i in range(input_unpack_sub_ele_num):
            # if unpack_i!=3:
            #     continue
            if dim_i==0:
                ele_unpack_code = f"[j for j in range({unpack_i + 1})]"
            elif dim_i==1:
                ele_unpack_code = f"[[k for k in range({unpack_i + 1})] for j in range({unpack_i + 1})]"

            input_code=f"input_seq=[{ele_unpack_code} for i in range({10**i})]\n"
            for_iter_code="for e in input_seq:\n"
            for subscript_i in range(1,subscript_num+1):
                for num_unpack in range(unpack_i+1):
                    if dim_i == 0:
                        benchmark_ele_list = [f'    e[{i}]\n' for i in range(unpack_i + 1)]
                    elif dim_i == 1:
                        benchmark_ele_list = [f'    e[{i}][{j}]\n' for i in range(unpack_i + 1) for j in range(unpack_i + 1)]

                    if dim_i == 0:
                        e_ele_list = [f'    e[{i}]\n' for i in range(num_unpack + 1)]
                    elif dim_i == 1:
                        e_ele_list = [f'    e[{i}][{j}]\n' for i in range(num_unpack + 1) for j in range(num_unpack + 1)]

                    for flag_i in [0,1]:
                        code_valid = 0
                        if flag_i:
                            if len(e_ele_list)>1:
                                all_e_list = [e_ele_list[i_e_real % (len(e_ele_list)-1)] for i_e_real, e_real in
                                              enumerate(range(subscript_i))]
                                flag_need_star =0
                                code_valid=1
                        else:
                            all_e_list = [e_ele_list[i_e_real % len(e_ele_list)] for i_e_real, e_real in
                                          enumerate(range(subscript_i))]
                            flag_need_star =1 if set(benchmark_ele_list)-set(all_e_list) else 0
                            if flag_need_star:
                                code_valid=1
                        if not code_valid:
                            continue
                        code = "    ".join(["    " + input_code, for_iter_code] + all_e_list)
                        code_complicated_str = func_def_str + code + if_main_str + "\n    print('code is finished')"
                        print(
                            f">>>{flag_need_star}flag_need_star;{10 ** i} input; {dim_i + 2} input dim; {unpack_i + 1} unpack_i;{subscript_i} subscript_i"
                            f">>>>>>>code_complicated_str: \n", code_complicated_str)
                        file_name = f"{flag_need_star}_flag_{10 ** i}_input_{dim_i + 2}_dim_{unpack_i + 1}_unpack_{subscript_i}_subscript_{num_unpack + 1}_uniqueUnpack_func.py"
                        file_name_list.add(file_name)
                        # util.save_file_path(bench_dir + file_name, code_complicated_str)
                        count += 1


                    # print("set(benchmark_ele_list)-set(all_e_list): ",set(benchmark_ele_list),set(all_e_list),set(benchmark_ele_list)-set(all_e_list))
                    # subscr_code="\n".join(all_e_list)

    # break
        # continue
print("total code: ",count,len(file_name_list))
#



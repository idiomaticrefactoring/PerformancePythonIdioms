import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util
func_def_str_var="def func_arg(*e):\n    pass\ndef func_a():\n    i=0"
func_def_str="def func_arg(*e):\n    pass\ndef func_a():\n"
if_main_str="\nif __name__ == '__main__':\n    func_a()"
bench_dir=util.data_root_mv + "lab_performance/call_star_benchmarks/code/code/"
num=30
ass_code=f'e_list=[i for i in range({num})]'
subscript_num_list=[i for i in range(2, num)]
step_list=[1,2]
file_name_list=set([])
count=0

for step in step_list:
    for i in range(0,num,step):
        if i==0 and step==2:
            continue
        # if i>3:
        #     break
        flag_no_end = 0
        sub_ele_list=[f"e_list[{e}]" for e in range(0,i+1,step)]
        sub_ele_list=["e_list[i]"]+[f"e_list[{i}+{e}]" for e in range(1,i+1,step)]

        if i==num-step:
            flag_no_end=1
        code=f"    {ass_code}\n    func_arg("+",".join(sub_ele_list)+")"
        code_complicated_str = func_def_str + code + if_main_str + "\n    print('code is finished')"
        file_name = f"{flag_no_end}_flag_{step}_step_{i}_end_func.py"
        print("code_complicated_str: \n")
        print(code_complicated_str)
        print(file_name)
        file_name_list.add(file_name)
        util.save_file_path(bench_dir + file_name, code_complicated_str)
        count +=1



            # break
        # continue
        # break
    # continue
print("total code: ",count,len(file_name_list))
#



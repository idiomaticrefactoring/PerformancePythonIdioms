import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util

import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util
func_def_str="def func_arg(*e):\n    pass\n"
if_main_str="\nif __name__ == '__main__':\n    "
bench_dir=util.data_root_mv + "lab_performance/call_star_benchmarks/code/code_new/"
bench_dir=util.data_root_mv + "lab_performance/call_star_benchmarks_paper/code/code_new/"

num=30

step_list=[1,2]
file_name_list=set([])
count=0
for num in list(range(2,31)):
    for lower in [0,1]:
        for step in step_list:

            ass_code = f'e_list=[i for i in range({num})]'
            subscript_num_list = [i for i in range(2, num)]

            for i in range(lower,num,step):
                # flag_no_end = 0
                # if i==0 and step==2:
                #     continue
                # if i>3:
                #     break

                for i_const in [0,1]:
                    flag_no_end = 0
                    if i_const==0 and lower==1:
                        continue

                    if i_const==0:
                        sub_ele_list = [f"e_list[i_s]"] + [f"e_list[i_s+{e}]" for e in range(step, i+1, step)]
                        if_main_str = f"\nif __name__ == '__main__':\n    i_s=0\n    "

                    else:
                        sub_ele_list = [f"e_list[{e}]" for e in range(lower, i+1, step)]
                        if_main_str = "\nif __name__ == '__main__':\n    "
                    if len(sub_ele_list)<=1:
                        continue
        # sub_ele_list=[f"e_list[{e}]" for e in range(0,i+1,step)]
                    if num%2:
                        if i == num - 1:
                            flag_no_end = 1
                    else:
                        if i == num - step and lower == 0 or i == num - 1 and lower == 1:
                            flag_no_end = 1

                    code=f"{ass_code}\n    func_arg("+",".join(sub_ele_list)+")"
                    code_complicated_str = func_def_str + if_main_str +code +  "\n    print('code is finished')"
                    if i_const==0:
                        file_name = f"{flag_no_end}_Endflag_{num}_num_var_lower_{step}_step_{len(sub_ele_list)}_subscript.py"
                    else:
                        file_name = f"{flag_no_end}_Endflag_{num}_num_{lower}_lower_{step}_step_{len(sub_ele_list)}_subscript.py"

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
bench_dir_sample=util.data_root_mv + "lab_performance/call_star_benchmarks_paper_sample_new/code/code_new/"
from random import sample
random.seed(2022)
sample_file_name_list=sample(file_name_list,960)
for file_name in sample_file_name_list:
    content = util.load_file_path(bench_dir + file_name)

    util.save_file_path(bench_dir_sample + file_name, content)


func_def_str_var="def func_arg(*e):\n    pass\ndef func_a():\n    i=0"
func_def_str="def func_arg(*e):\n    pass\ndef func_a():\n"
if_main_str="\nif __name__ == '__main__':\n    func_a()"
# bench_dir=util.data_root_mv + "lab_performance/call_star_benchmarks/code/code_new/"
# num=30
# ass_code=f'e_list=[i for i in range({num})]'
# subscript_num_list=[i for i in range(2, num)]
step_list=[1,2]
file_name_list=set([])
count_code=0
count=0
for num in list(range(2,31)):
    for lower in [0, 1]:
        for step in step_list:
            ass_code = f'e_list=[i for i in range({num})]'

            for i in range(lower,num,step):

                # if i>3:
                #     break
                for i_const in [0,1]:
                    if i_const==0 and lower==1:
                        continue
                    if i_const==0:
                        sub_ele_list = [f"e_list[i_s]"] + [f"e_list[i_s+{e}]" for e in range(step, i+1, step)]

                        func_def_str = "def func_arg(*e):\n    pass\ndef func_a():\n    i_s=0\n"


                    else:
                        sub_ele_list = [f"e_list[{e}]" for e in range(lower, i+1, step)]
                        func_def_str = "def func_arg(*e):\n    pass\ndef func_a():\n"

                    if len(sub_ele_list)<=1:
                        continue
                    flag_no_end = 0
                    if num%2:
                        if i == num - 1:
                            flag_no_end = 1
                    else:
                        if i == num - step and lower==0 or i == num - 1 and lower==1:
                            flag_no_end = 1

                    code=f"    {ass_code}\n    func_arg("+",".join(sub_ele_list)+")"
                    code_complicated_str = func_def_str + code + if_main_str + "\n    print('code is finished')"
                    print("num: ",num)
                    if i_const==0:
                        file_name = f"{flag_no_end}_Endflag_{num}_num_var_lower_{step}_step_{len(sub_ele_list)}_subscript_func.py"
                    else:
                        file_name = f"{flag_no_end}_Endflag_{num}_num_{lower}_lower_{step}_step_{len(sub_ele_list)}_subscript_func.py"

                    print("code_complicated_str: \n")
                    if file_name[:-8]+".py" in sample_file_name_list:
                        print(code_complicated_str)
                        print(file_name)
                        file_name_list.add(file_name)
                        util.save_file_path(bench_dir_sample + file_name, code_complicated_str)
                        count +=1



            # break
        # continue
        # break
    # continue
print("total code: ",count,len(file_name_list))

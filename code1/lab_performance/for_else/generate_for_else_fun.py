import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util
count=0
file_name_list=set([])
all_file_name_list=[]
func_def_str="def func_a():\n"
if_main_str="\nif __name__ == '__main__':\n    func_a()"
input_num_list=[10**i for i in range(7)]
threshold=10
node_kind_list=[["for i in e_list:\n"], ["while i:\n"]]

else_body_list=[[f"if flag==True:\n","    pass\n"],[f"if flag==True:\n","    pass\n","else:\n","    pass\n"]]
# ass_code=f"e_list=[i for i in range({input_num})]\n flag=True"
# if_body=f"    if i=={input_num-1}:\n    flag=False\n    break\n"
# else_body=f"if flag==True:\n    pass"
# else_body_2=f"if flag==True:\n    pass\nelse:\n    pass"
bench_dir=util.data_root_mv + "lab_performance/for_else_benchmarks/code/code/"

for input_num in input_num_list:
    for node_kind in node_kind_list:
        # print(">>>>>>>node_kind: ",node_kind)
        if "for i in e_list:\n" in node_kind:
            branch_list = [[f"    if i=={input_num}:\n", "        flag=False\n", "        break\n"],
                           [f"    if i=={input_num - 1}:\n", "        flag=False\n", "        break\n"]
                           ]
            ass_code = [f"    e_list=[i for i in range({input_num})]\n", "flag=True\n"]
            node_kind_name="for"
            # print(">>>>>>>>>>>>>>>>>>come here")
        else:
            ass_code = [f"    i={input_num}\n", "flag=True\n"]
            branch_list = [
                ["    i-=1\n", f"    if i=={-1}:\n", "        flag=False\n", "        break\n"],
                ["    i-=1\n", f"    if i=={0}:\n", "        flag=False\n", "        break\n"]]
            node_kind_name = "while"
        for ind_branch,branch in enumerate(branch_list):
            for ind_else,else_body in enumerate(else_body_list):
                code="    ".join(ass_code+node_kind+branch+else_body)
                code_complicated_str = func_def_str + code + if_main_str + "\n    print('code is finished')"
                # print("********************")
                # print(code_complicated_str)
                file_name = f"{input_num}_inputNum_{node_kind_name}_nodeKind_{ind_branch}_break_{ind_else}_else_func.py"
                # print("code_complicated_str: \n")
                # print(code_complicated_str)
                # print(file_name)
                util.save_file_path(bench_dir + file_name, code_complicated_str)

                file_name_list.add(file_name)
                all_file_name_list.append(file_name)
                count += 1
                # break

            # break
        # break
    # break
print("total code: ",count,len(file_name_list),file_name_list,all_file_name_list)

#
#         file_name = f"{flag_no_end}_flag_{step}_step_{i}_end_func.py"
#         print("code_complicated_str: \n")
#         print(code_complicated_str)
#         print(file_name)
#         file_name_list.add(file_name)
#         util.save_file_path(bench_dir + file_name, code_complicated_str)
#         count +=1
#             # break
#         # continue
#         # break
#     # continue
# print("total code: ",count,len(file_name_list))
#



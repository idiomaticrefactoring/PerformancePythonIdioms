import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util
bench_dir=util.data_root_mv + "lab_performance/truth_value_test_benchmarks/code/code/"

count=0
file_name_list=set([])
all_file_name_list=[]
func_def_str=""
if_main_str="\nif __name__ == '__main__':\n"
empty_list = ["None", "False", "0", "0.0", "0j", "Decimal(0)", "Fraction(0, 1)", '', "()", "[]", "{}", "dict()",
              "set()", "range(0)"]
node_list=["if","assert","while"]
branch_true_false=["==","!="]
for empty in empty_list:
    for equal_flag in branch_true_false:
        for node in node_list:
            if empty=='':
                print("empty is ",empty)
                if "Decimal" in empty:
                    ass_code = [f"    from decimal import Decimal\n", f"a = ''\n"]
                elif "Fraction" in empty:
                    ass_code = [f"    from fractions import Fraction\n", f"a = ''\n"]

                else:

                    ass_code = [f"    a = ''\n"]
                print("ass_code: ", ass_code)
                if node == "if":
                    node_code = [f"{node} a {equal_flag} '':\n", "    pass\n"]
                elif node == "while":
                    node_code = [f"{node} a {equal_flag} '':\n", "    break\n"]
                elif node == "assert":
                    node_code = ["try:\n", f"    {node} a {equal_flag} ''\n", "except:\n", "    pass"]

            else:
                if "Decimal" in empty:
                    ass_code=[f"    from decimal import Decimal\n",f"a = {empty}\n"]
                elif "Fraction" in empty:
                    ass_code = [f"    from fractions import Fraction\n", f"a = {empty}\n"]

                else:

                    ass_code=[f"    a = {empty}\n"]
                print("ass_code: ",ass_code)
                if node=="if":
                    node_code=[f"{node} a {equal_flag} {empty}:\n","    pass\n"]
                elif node=="while":
                    node_code = [f"{node} a {equal_flag} {empty}:\n", "    break\n"]
                elif node=="assert":
                    node_code = ["try:\n",f"    {node} a {equal_flag} {empty}\n","except:\n","    pass"]

            code="    ".join(ass_code+node_code)
            code_complicated_str = func_def_str + if_main_str + code + "\n    print('code is finished')"

            print("code_complicated_str: \n")
            print(code_complicated_str)
            file_name = f"{empty}_empty_{equal_flag}_equal_flag_{node}_node.py"
            file_name_list.add(file_name)
            util.save_file_path(bench_dir + file_name, code_complicated_str)
            # break
        # break
    # break
print("total code: ",count,len(file_name_list))

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
#



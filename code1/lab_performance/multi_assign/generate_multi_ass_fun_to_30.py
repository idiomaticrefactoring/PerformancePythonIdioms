import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util

var_1_copy=1
var_2_copy=2
var_1=1
var_2=2

var_1=var_1_copy
var_2=var_2_copy
len_ass=31
var_list=['var_'+str(i) for i in range(1,len_ass)]
var_copy_list=['var_'+str(i)+"_copy" for i in range(1,len_ass)]
ass_const_list=['var_'+str(i)+" = "+str(i)  for i in range(1,len_ass)]
ass_var_list=['var_'+str(i)+" = "+'var_'+str(i)+"_copy"  for i in range(1,len_ass)]
ass_copy_list=['var_'+str(i)+"_copy"+" = "+str(i)  for i in range(1,len_ass)]
tmp_list=['tmp_'+str(i) for i in range(1,len_ass)]
tmp_ass_list=['tmp_'+str(i)+" = "+'var_'+str(i) for i in range(1,len_ass)]


func_def_str="def func_a():\n"
if_main_str="\nif __name__ == '__main__':\n    func_a()"
bench_dir=util.data_root + "lab_performance/multi_ass_benchmarks_30/code/code/"
count=0
for i in range(2,len_ass):
    const_file_name=f"{i}_ass_const_func.py"
    var_ass_list=ass_const_list[:i]
    code_list = var_ass_list
    code_list = ["    " + code for code in code_list]
    code = "\n".join(code_list)
    code_complicated_str = func_def_str +code + if_main_str+"\n    print('code is finished')"
    print(f">>>>>>>>{i} const code: \n{code_complicated_str}")
    util.save_file_path(bench_dir+const_file_name, code_complicated_str)

    var_file_name = f"{i}_ass_var_func.py"
    var_ass_list = ass_var_list[:i]
    code_list = ass_copy_list[:i]+['pass']+var_ass_list
    code_list = ["    " + code for code in code_list]
    code = "\n".join(code_list)
    code_complicated_str = func_def_str + code + if_main_str+"\n    print('code is finished')"
    print(f">>>>>>>>{i} var ass code: \n{code_complicated_str}")
    util.save_file_path(bench_dir+var_file_name, code_complicated_str)

    var_swap_file_name = f"{i}_ass_swap_func.py"
    pre_ass_list = ass_const_list[:i]+["pass"]
    # pre_ass="\n".join(var_ass_list)
    var_ass_list = ass_const_list[:i]
    tmp_ass_pre = tmp_ass_list[:i-1]
    swap_ass=[var+" = "+tmp_list[ind] for ind,var in enumerate(var_list[1:i])]
    code_list=pre_ass_list+tmp_ass_pre+['var_1 = '+var_list[i-1]]+swap_ass
    code_list=["    "+code for code in code_list]
    code = "\n".join(code_list)
    code_complicated_str = func_def_str + code+ if_main_str+"\n    print('code is finished')"
    print(f">>>>>>>>{i} swap ass code: \n{code_complicated_str}")
    util.save_file_path(bench_dir+var_swap_file_name, code_complicated_str)

    count+=3
print("count: ",count)
    # if i>3:
    #     break
    # save_path = bench_dir + code + '_func.py'
    # print(save_path)
    # util.save_file_path(save_path, code_complicated_str)


'''
for ind,(e1,e2) in enumerate(comb_1):
    # if ind not in sample_index:
    #     continue
    print((e1,e2))
    var_list = set([])
    code_complicated_str = ""
    code1=code_str_chain_compare_list_1[e1][0][1]
    var_list |= set(re.split(split_patt, code1))
    code2=""
    code2_list = code_str_chain_compare_list_2[e2]
    for compare_str, e_code3 in code2_list:
        if compare_str in code1:
            code2 = e_code3
            var_list |= set(re.split(split_patt, code2))
            break
    if not code2:
        continue
    var_str = get_var_defintion_str(var_list)
    print("var_list: ", var_str)
    code = code1 + " and " + code2
    code_var = var_str + "\n    " + code
    code_complicated_str = func_def_str + code_var + if_main_str+"\n    print('code is finished')"
    save_path = bench_dir + code + '_func.py'
    print(save_path)
    count += 1
    util.save_file_path(save_path, code_complicated_str)
    print(code_complicated_str)
    # break
sample_index=random.sample(range(0,len(comb_1)), 20)

for ind,(e1,e2,e3) in enumerate(comb_2):
    # if ind not in sample_index:
    #     continue
    print((e1,e2,e3))
    code_complicated_str = ""
    var_list=set([])
    code2=""
    code1 = code_str_chain_compare_list_1[e1][0][1]
    var_list |= set(re.split(split_patt, code1))
    code2_list = code_str_chain_compare_list_2[e2]
    for compare_str,e_code3 in code2_list:
        if compare_str in code1:
            code2=e_code3
            var_list|=set(re.split(split_patt,code2))
            break
    code3_list = code_str_chain_compare_list_3[e3]
    code3=""
    for compare_str,e_code3 in code3_list:
        if compare_str in code1.split(" "):
            code3=e_code3
            var_list|=set(re.split(split_patt,code3))
            break
        elif compare_str in code2.split(" "):
            code3 = e_code3
            var_list |= set(re.split(split_patt, code3))
            break

    if not code3:
        continue
    var_str=get_var_defintion_str(var_list)
    print("var_list: ",)
    code = code1 + " and " + code2+ " and " + code3
    code_var=var_str+"\n    "+code
    code_complicated_str = func_def_str + code_var + if_main_str+"\n    print('code is finished')"
    save_path = bench_dir + code + '_func.py'
    print(save_path)
    count += 1
    util.save_file_path(save_path, code_complicated_str)
    print(code_complicated_str)
    # break
print("total code: ",count)
'''
#



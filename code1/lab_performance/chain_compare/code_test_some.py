import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util
iterable=[i for i in range(10)]
code_str_chain_compare_list_1=[[(">=","e>=three")],
[(">","e>three")],
[("<","e<ten")],
[("<=","e<=ten")],
[("==","e==five")],
[("!=","e!=ten")],
[("is","e is five")],
[("is not","e is not ten")],
[("in","e in b_list")],
[("not in","e not in a_list")]]

code_str_chain_compare_list_2=[[("e","ten_2>=e")],
[("e","ten_2>e")],
[("e","three_2<=e")],
[("e","three_2<e")],
[("e","five_2==e")],
[("e","ten_2!=e")],
[("e","five_2 is e")],
[("e","ten_2 is not e")],
[("a_list","a_list in a_list_list"),
 ("b_list","b_list in b_list_list"),("e","e in b_list")],
[("a_list","a_list not in b_list_list"),("b_list","b_list not in a_list_list"),
 ("e","e not in a_list")]
 ]

code_str_chain_compare_list_3=[[("three","three>=two_3"),("ten","ten>=twenty_3"),("five","five>=two_3"),
 ("three_2","three_2>=twenty_3"),
 ("ten_2","ten_2>=twenty_3"),
 ("five_2","five_2>=twenty_3")],


[("three","three>two_3"),("ten","ten>twenty_3"),("five","five>two_3"),
("three_2", "three_2>twenty_3"), ("ten_2", "ten_2>twenty_3"),
 ("five_2", "five_2>twenty_3")],

[("three","three<=twenty_3"),("ten","ten<=twenty_3"),("five","five<=twenty_3"),
 ("three_2","three_2<=twenty_3"),("ten_2","ten_2<=twenty_3"),
 ("five_2","five_2<=twenty_3")],
[("three","three<twenty"),("ten","ten<twenty"),("five","five<twenty"),
 ("three_2","three_2<twenty_3"),("ten_2","ten_2<twenty_3"),
 ("five_2","five_2<twenty_3")],
[("five","five==five_3"),("three","three==three_3"),("ten","ten==ten_3"),
 ("three_2", "three_2==three_3"), ("ten_2", "ten_2==ten_3"),
 ("five_2", "five_2==five_3")],

[("three","three!=twenty_3"),("ten","ten!=twenty_3"),("five","five!=twenty_3"),
 ("three_2", "three_2!=twenty_3"), ("ten_2", "ten_2!=twenty_3"),
 ("five_2", "five_2!=twenty_3")],

[("three","three is three_3"),("ten","ten is ten_3"),("five","five is five_3"),
 ("three_2", "three_2 is three_3"), ("ten_2", "ten_2 is ten_3"),
 ("five_2", "five_2 is five_3")],

[("is not","three is not twenty_3"),("is not","ten is not twenty_3"),
 ("is not","five is not twenty_3"),
 ("three_2", "three_2 is not twenty_3"), ("ten_2", "ten_2 is not twenty_3"),
 ("five_2", "five_2 is not twenty_3")],
[
 ("a_list_list","a_list_list in a_list_list_list"),
("b_list_list","b_list_list in b_list_list_list"),
    ("a_list","a_list in a_list_list"),
("b_list","b_list in b_list_list"),
("three","three in a_list"),("five","five in a_list"),
    ("ten","ten in a_list"),
    ("three_2", "three_2 in a_list"), ("ten_2", "ten_2 in a_list"),
    ("five_2", "five_2  in a_list")],
[("a_list_list","a_list_list not in b_list_list_list"),
("a_list","a_list not in b_list_list_list"),
("b_list_list","b_list_list not in a_list_list_list"),
("b_list","b_list not in a_list_list"),
("three","three not in b_list"),("five","five not in b_list"),
("ten","ten not in b_list"),
 ("three_2", "three_2 not in b_list"),
 ("ten_2", "ten_2 not in b_list"),
 ("five_2", "five_2 not in b_list")]]
dict_var={
    "a":"a=1","b":"b=2","c":"c=3","d":"d=4","e":"e=5",
    "one":"one=1","two":"two=2","three":"three=3","four":"four=4",
    "five":"five=5","ten":"ten=10","twenty":"twenty=20",
    "one_2": "one_2=1", "two_2": "two_2=2", "three_2": "three_2=3", "four_2": "four_2=4",
             "five_2": "five_2=5","ten_2":"ten_2=10","twenty_2":"twenty_2=20",
    "one_3": "one_3=1", "two_3": "two_3=2", "three_3": "three_3=3",
    "four_3": "four_3=4", "five_3": "five_3=5","ten_3":"ten_3=10","twenty_3":"twenty_3=20",
    "a_list":"a_list=[1,2,3]","b_list":"b_list=[4,5,6]",
    "a_list_list": "a_list_list=[[1,2,3]]", "b_list_list":"b_list_list=[[4,5,6]]" ,
    "a_list_list_list": "a_list_list_list=[[[1,2,3]]]", "b_list_list_list": "b_list_list_list=[[[4,5,6]]]",

}
split_patt=r"<=|>=|not in|is not|==|!=|<|>|is |in |and"
def get_var_defintion_str(var_list):
    var_list={e.strip() for e in var_list}
    var_str_list=[]
    for var in var_list:
        var_str_list.append("    "+dict_var[var])
    return "\n".join(var_str_list)

comb_1=itertools.combinations_with_replacement(iterable, 2)
comb_2=itertools.combinations_with_replacement(iterable, 3)
comb_1=list(comb_1)
comb_2=list(comb_2)
func_def_str="def func_a():\n"
if_main_str="\nif __name__ == '__main__':\n    func_a()"
bench_dir=util.data_root + "lab_performance/chain_compare_benchmarks/code/code/"
count=0
sample_index=random.sample(range(0,len(comb_1)), 20)
for ind,(e1,e2) in enumerate(comb_1):
    if ind not in sample_index:
        continue
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
    code_complicated_str = func_def_str + code_var + if_main_str
    save_path = bench_dir + code + '_func.py'
    print(save_path)
    count += 1
    # util.save_file_path(save_path, code_complicated_str)
    print(code_complicated_str)
    # break
sample_index=random.sample(range(0,len(comb_1)), 20)

for ind,(e1,e2,e3) in enumerate(comb_2):
    if ind not in sample_index:
        continue
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
        if compare_str in code1:
            code3=e_code3
            var_list|=set(re.split(split_patt,code3))
            break
        elif compare_str in code2:
            code3 = e_code3
            var_list |= set(re.split(split_patt, code3))
            break

    if not code3:
        continue
    var_str=get_var_defintion_str(var_list)
    print("var_list: ",)
    code = code1 + " and " + code2+ " and " + code3
    code_var=var_str+"\n    "+code
    code_complicated_str = func_def_str + code_var + if_main_str
    save_path = bench_dir + code + '_func.py'
    print(save_path)
    count += 1
    # util.save_file_path(save_path, code_complicated_str)
    print(code_complicated_str)
    # break
#



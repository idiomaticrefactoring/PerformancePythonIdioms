import itertools,random,re

import time
import sys,ast,os,csv,time
import subprocess
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
import util
small = {chr(i):i for i in range(97,123)}
bench_dir=util.data_root + "lab_performance/chain_compare_benchmarks_new/code/code/"
bench_dir=util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/code/code/"

print(small)
def idiom_to_non_idiom(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            new_node = ast.BoolOp()
            new_node.op = ast.And()
            new_node.values = []

            node.comparators.insert(0, node.left)
            for ind in range(1, len(node.comparators)):  # node.comparators[1:]:

                compare_node = ast.Compare()
                compare_node.left = node.comparators[ind - 1]
                compare_node.ops = node.ops[ind - 1:ind]
                compare_node.comparators = node.comparators[ind:ind + 1]
                # print("compare node: ",ast.unparse(compare_node))
                new_node.values.append(compare_node)
            print("code: ", ast.unparse(new_node))
            return ast.unparse(new_node)
# a=["<=",">=","not in","is not","==","!=","<",">","is","in"]
iterable=[i for i in range(10)]
code_list=[]
file_name_list=[]
a=["<=",">=","==","!=","<",">","not in","in","is","is not"]
dict_comp_map={
"<=":">",">=":"<","==":"!=","!=":"==",
"<":">=",">":"<=","not in":"in","in":"not in",
"is":"is not","is not":"is"
}

def get_var(op):
    for ee_op in op:
        if str.isalpha(ee_op):
            return ee_op
count_num_comb=0
for i in range(2,6):
    comb_1=itertools.combinations_with_replacement(a, i)

    comb_1=list(comb_1)
    print(len(list(comb_1)))
    count_num_comb+=len(list(comb_1))
    continue


    for ind,comb_e in enumerate(comb_1):

        for change_ind  in [-1,len(comb_e)-1]:#range(-1,len(comb_e)):#len(comb_e)

            op_list = ["n"]
            dict_map_var = dict()
            # code_str="a"
            code_str = "n "
            ass_extra=[]
            real_ind = None
            pos_is_not=None
            for ind_comp, comp in enumerate(comb_e[:]):


                op_str=op_list[-1]
                if comp=="<=" or comp=="<" or comp=="!=":
                        if "[" in op_str:
                            break
                        another_op=chr(ord(op_str)+1)

                elif comp==">=" or comp==">":
                    if "[" in op_str:
                        break
                    another_op = chr(ord(op_str) - 1)
                elif comp=="==" :
                    another_op =op_str
                elif comp=="not in":
                    op_str_split=op_str.split(" ")
                    for ind_e_op,e_op in enumerate(op_str_split):
                         if str.isalpha(e_op):
                             op_str_split[ind_e_op]=chr(ord(e_op) + 1)
                             break
                    another_op ="".join(['[' ," ".join(op_str_split),']'])
                elif comp=="is":

                    # if "[" in op_str and real_ind is None :
                    #     real_ind = [ind_comp]
                    # elif "[" in op_str:
                    #     real_ind.append(ind_comp)
                        # another_op = op_str
                        # another_op=get_var(op_str)+"_copy"
                        # ass_extra.append(f"    {another_op}={op_str}")
                        # real_ind=change_ind
                    # else:
                    another_op =op_str
                elif comp=="is not":

                    # real_ind = ind_comp - 1
                    # if "[" in op_str and pos_is_not is None:
                    #     pos_is_not = ind_comp
                    #     real_ind = ind_comp - 1
                        # break
                        # real_ind = ind_comp - 1

                    op_str_split = []
                    for ind_e_op, e_op in enumerate(op_str):
                        if str.isalpha(e_op):

                            op_str_split.append( chr(ord(e_op) + 1))
                            # break
                        else:
                            op_str_split.append( e_op)
                    another_op = " ".join(op_str_split)
                    print("another_op: ",op_str,another_op)
                elif comp=="in":
                    another_op = "".join(['[', op_str, ']'])
                    # dict_map[another_op]=get_var(another_op)+f"_list_{len(dict_map)}"
                    # ass_extra.append()
                if change_ind==ind_comp:
                    comp=dict_comp_map[comp]
                    # if real_ind is not None and comp=="is not":
                    #     index_fuzhu=real_ind.index(ind_comp)
                    #     real_ind[index_fuzhu]=len(comb_e)

                    # elif  pos_is_not is not None and comp=="is":
                    #     real_ind = pos_is_not


                # else:
                #     if real_ind is not None and comp == "is":
                #         real_ind = real_ind

                op_list.append(another_op)
                code_str += comp + " "
                code_str+=another_op+" "

            else:
                # print(code_str)
                # if real_ind is not None:
                #     real_ind = real_ind[0]
                # elif pos_is_not is not None:
                #     real_ind = pos_is_not
                print("******************")
                print(code_str)
                code_str=idiom_to_non_idiom(code_str)
                assign_list=[]
                right_value_ass_list=[]
                exist_op_list=[]
                for op in op_list:

                    if str.isalpha(op):
                        assign_str="    "+op+"="+str(ord(op))
                        if assign_str not in assign_list:
                            assign_list.append(assign_str)
                            right_value_ass_list.append(str(ord(op)))
                    elif "]" in op:
                        for ee_op in op:
                            if str.isalpha(ee_op):
                                assign_str = "    " + ee_op + "=" + str(ord(ee_op))
                                right_value_ass_list.append(str(ord(ee_op)))
                                if assign_str not in assign_list:
                                    assign_list.append(assign_str)
                                break
                    k= op.count("]")
                    if k>=1 and op not in exist_op_list:
                        right_e=f"[{get_var(op)}]"
                        if right_e not in dict_map_var:
                            left_e=f'list_{len(dict_map_var)}'
                            assign_str=f"    {left_e}={right_e}"
                            dict_map_var[right_e] = left_e

                            assign_list.append(assign_str)
                        # if assign_str not in assign_list:
                        #     dict_map_var[right_e]=f"list_{len(dict_map_var)}"
                                # \
                                # .append([f"[{get_var(op)}]",f"list_{len(dict_map_var)}"])
                            # assign_list.append(assign_str)
                            # right_value_ass_list.append(right_e)
                        if k>=2:
                            for i_list_construct in range(1,k):
                                current=f"{'[' * (i_list_construct + 1)}{get_var(op)}{']' * (i_list_construct + 1)}"
                                pre=f"{'[' * (i_list_construct)}{get_var(op)}{']' * (i_list_construct)}"
                                # right_e = f"[list_{len(dict_map_var)-1}]"

                                if current not in dict_map_var:
                                    left_e = f'list_{len(dict_map_var)}'
                                    assign_str = f"    {left_e}=[{dict_map_var[pre]}]"
                                    dict_map_var[current] = left_e

                                    # dict_map_var.append([f"{'['*(i_list_construct+1)}{get_var(op)}{']'*(i_list_construct+1)}",f"list_{len(dict_map_var)}"])
                                    assign_list.append(assign_str)
                                    # right_value_ass_list.append(right_e)
                    exist_op_list.append(op)
                # assign_list=set(ass_extra)|assign_list
                # dict_map_var=sorted(dict_map_var,key=(lambda x:x[0].count("[")),reverse=True)
                dict_map_var=sorted(dict_map_var.items(), key=lambda kv: kv[0].count("]"),reverse=True)
                print(dict_map_var)
                for old_ass,new_ass in dict_map_var:
                    code_str=code_str.replace(old_ass,new_ass)

                assign_code="\n".join(assign_list)

                complicate_code=assign_code+"\n    "+code_str


                func_def_str = ""
                if_main_str = "\nif __name__ == '__main__':\n"
                code_complicated_str = func_def_str + if_main_str + complicate_code + "\n    print('code is finished')"
                ind_true=str(len(comb_e))  if change_ind==-1 else str(change_ind)
                code_file_name = ind_true+"_"+"_".join(comb_e)+".py"
                save_path = bench_dir + code_file_name
                file_name_list.append(save_path)
                # util.save_file_path(save_path, code_complicated_str)
                code_list.append(complicate_code)

                print(code_complicated_str)
                print("code_file_name: ",dict_map_var,code_file_name)

                func_def_str = "def func_a():\n"
                if_main_str = "\nif __name__ == '__main__':\n    func_a()"
                code_complicated_str = func_def_str + complicate_code + if_main_str + "\n    print('code is finished')"
                code_file_name=ind_true+"_"+"_".join(comb_e)+"_func.py"
                print(op_list,code_complicated_str)
                print("code_file_name: ",dict_map_var,code_file_name)
                save_path = bench_dir + code_file_name
                file_name_list.append(save_path)
                # util.save_file_path(save_path, code_complicated_str)
                code_list.append(code_complicated_str)

print("code: ",len(code_list),len(file_name_list),count_num_comb)



# print(chr(110))

# print(len(list(comb_1)))
# comb_2=itertools.combinations_with_replacement(iterable, 3)
# comb_1=list(comb_1)
# comb_2=list(comb_2)
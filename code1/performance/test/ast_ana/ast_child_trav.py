import copy
import sys,ast,os,csv,time,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-4])+"/"
print("code_dir: ",code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir+"lab_performance/")
# sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"test_case/")
import util,get_test_case_acc_util,performance_util,configure_pro_envir_util
import code_info
from extract_simp_cmpl_data import ast_util
import ast_performance_util
# import replace_content_by_ast_time_percounter
import performance_replace_content_by_ast_add_type

if __name__ == '__main__':
#for line in itertools.islice(data, 100):
    # temp_list.append(line)
    code='''
for val in series:
    if val is None:
        newValues.append(None)
    elif val <= 0:
        newValues.append(None)
    else:
        newValues.append(math.log(val, base))
for elem in root:
    if elem.tag != gc.CONFIG_XML_TASKS_TAG and elem.text is not None:
        pairs.append(u'%s%s%s' % (safe_unicode(elem.tag), gc.CONFIG_STRING_ASSIGNMENT_SYMBOL, safe_unicode(elem.text.strip())))    
    '''

    for node in ast.walk(ast.parse(code)):
        if isinstance(node,ast.For):
            child =node
            break
    names = []
    real_list=[]
    func_call_list=[]
    util.visit_vars(child, names)
    util.visit_vars_real(child, real_list)
    util.visit_func_call_real(child,func_call_list)
    print(names,"\n",real_list,"\n",func_call_list)
    pass

import os,sys
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
import util
from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
from transform_c_s import transform_chained_comparison_compli_to_simple
from tokenize import tokenize
import ast,traceback,copy
def refactor_chain_compare(file_path):

    content = util.load_file_path(file_path)
    new_code_list=[]
    try:
        tree=ast.parse(content)
        new_code_list = []
        for node in ast.walk(tree):
            if isinstance(node, ast.BoolOp):
                op = node.op
                old_node = copy.deepcopy(node)
                print(ast.unparse(old_node))
                if isinstance(op, ast.And):
                    values = node.values
                    simple_node=[ast.unparse(values[0])]
                    for value in values[1:]:
                        if isinstance(value, ast.Compare):
                            left = value.left
                            comparator = value.comparators[-1]
                            value_str=ast.unparse(value)
                            value_str=" ".join( value_str.split(" ")[:-1])
                            value_str=value_str.replace(ast.unparse(left),"",1)
                            # value_str=value_str[::-1].replace(ast.unparse(comparator), "",1)
                            # print(value_str)
                            # value_str=value_str[::-1]
                            # print(ast.unparse(value.ops[0].__class__()),value.ops[0].__init__(),value.ops[0].__repr__(),value.ops[0].__class__(),value.ops[0].__str__())
                            simple_node.append(value_str)
                            simple_node.append(ast.unparse(comparator))
                    #         vars = [[ast.unparse(left), ast.unparse(comparator)], value]
                    #         vars_list.append(vars)
                    # transform_chained_comparison_compli_to_simple.check_chained_comparison(tree, new_code_list)
                    #
                break
        simple_node_str=" ".join(simple_node)
        for node in ast.walk(ast.parse(simple_node_str)):
            if isinstance(node, ast.Compare):
                # print(ast.unparse(node))
                new_code_list.append([old_node,node])
                break
    except:
        traceback.print_exc()
    return new_code_list
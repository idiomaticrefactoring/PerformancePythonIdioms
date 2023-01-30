import sys, ast, os, copy
import tokenize
import sys
import traceback

sys.path.append("..")
sys.path.append("../../")
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
sys.path.append(code_dir+"transform_c_s/")
import ast_performance_util


import time
import copy
import util,github_util
from extract_simp_cmpl_data import ast_util
class TimerStmt():
    def __init__(self):
        self.import_time_stmt = "import time"
        self.total_init_time_stmt = "total_time_zejun=0"
        self.start_time_stmt = "start_time_zejun=time.perf_counter()"
        self.end_time_stmt = "end_time_zejun=time.perf_counter()"
        self.diff_time_stmt = "total_time_zejun=end_time_zejun-start_time_zejun"
        self.total_time_stmt = "total_time_zejun+=end_time_zejun-start_time_zejun"
        self.print_total_stmt = 'print("\\n*********zejun test total time************** ", total_time_zejun)'
        self.print_total_stmt_pythonic = 'print("\\n*********zejun test total time pythonic************** ", total_time_zejun)'
        for node in ast.walk(ast.parse(self.import_time_stmt)):
            if isinstance(node, ast.Import):
                self.import_time_stmt = node
                break
        for node in ast.walk(ast.parse(self.diff_time_stmt)):
            if isinstance(node, ast.Assign):
                self.diff_time_stmt = node
                break
        for node in ast.walk(ast.parse(self.total_init_time_stmt)):
            if isinstance(node, ast.Assign):
                self.total_init_time_stmt = node
                break
        for node in ast.walk(ast.parse(self.start_time_stmt)):
            if isinstance(node, ast.Assign):
                self.start_time_stmt = node
                break
        for node in ast.walk(ast.parse(self.end_time_stmt)):
            if isinstance(node, ast.Assign):
                self.end_time_stmt = node
                break
        for node in ast.walk(ast.parse(self.total_time_stmt)):
            if isinstance(node, (ast.Assign, ast.AugAssign)):
                self.total_time_stmt = node
                break
        for node in ast.walk(ast.parse(self.print_total_stmt)):
            if isinstance(node, (ast.stmt)):
                self.print_total_stmt = node
                break
        for node in ast.walk(ast.parse(self.print_total_stmt_pythonic)):
            if isinstance(node, (ast.stmt)):
                self.print_total_stmt_pythonic = node
                break
class Rewrite(ast.NodeTransformer):
    def __init__(self,node,new_node,node_simple,new_node_simple):
        self.old_node =node
        self.new_node =new_node
        self.old_node_simple = node_simple
        self.new_node_simple = new_node_simple

        self.flag = 0
        TimerStmt.__init__(self)

    def generic_visit(self, node):
        if hasattr(node, "body"):
            # print("node: ",ast.unparse(node))
            ass_re = None
            for ind, child in enumerate(node.body):
                if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):

                    if self.import_time_stmt in node.body:
                        break
                    # print("yes, it is a call node: ", ast.unparse(child))

                    index = node.body.index(child)
                    # node.body.remove(child)
                    node.body.insert(index, self.print_total_stmt_pythonic)
                    node.body.insert(index, self.diff_time_stmt)
                    node.body.insert(index, self.end_time_stmt)
                    node.body.insert(index, self.new_node_simple)
                    node.body.insert(index, self.start_time_stmt)
                    node.body.insert(index, self.import_time_stmt)

                    self.flag = 1
                    break

                node.body[ind] = self.generic_visit(child)
        if hasattr(node, "orelse") and not self.flag:
            # print("come here: ",ast.unparse(node))
            for ind, child in enumerate(node.orelse):
                try:
                    if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):
                        if self.import_time_stmt in node.orelse:
                            break


                        index = node.orelse.index(child)
                        # node.orelse.remove(child)
                        node.orelse.insert(index, self.print_total_stmt_pythonic)
                        node.orelse.insert(index, self.diff_time_stmt)
                        node.orelse.insert(index, self.end_time_stmt)
                        node.orelse.insert(index, self.new_node_simple)
                        node.orelse.insert(index, self.start_time_stmt)
                        node.orelse.insert(index, self.import_time_stmt)
                        self.flag = 1
                        break
                    node.orelse[ind] = self.generic_visit(child)
                except:
                    traceback.print_exc()
        # if hasattr(node, "lineno"):
        #     if node.lineno == self.old_node.lineno and ast.unparse(node) == ast.unparse(self.old_node):
        #         print("come here")
        #
        #         return self.new_node
        # for ind_field, k in enumerate(node._fields):
        #     # print("transfrom: ", k)
        #     try:
        #
        #         # if 1:
        #         v = getattr(node, k)
        #         # print("here: ", k,v )
        #         if isinstance(v, ast.AST):
        #             if v._fields:
        #                 setattr(node, k, self.generic_visit(v))
        #             # node._fields[k] = self.generic_visit(v)
        #             pass
        #         elif isinstance(v, list):
        #
        #             for ind, e in enumerate(v):
        #                 if hasattr(e, '_fields'):
        #                     v[ind] = self.generic_visit(e)
        #             setattr(node, k, v)
        #             # node._fields[k][ind]=self.generic_visit(e)
        #             # pass
        #     except:
        #         continue

        return node
class Rewrite_add_unpack_starred(ast.NodeTransformer):
    def __init__(self,node,new_node,node_simple,new_node_simple):
        self.old_node =node
        self.new_node =new_node
        self.old_node_simple = node_simple
        self.new_node_simple = new_node_simple

        self.flag = 0
        TimerStmt.__init__(self)

    def generic_visit(self, node):
        if hasattr(node, "body"):
            # print("node: ",ast.unparse(node))
            ass_re = None
            for ind, child in enumerate(node.body):
                if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):

                    if self.import_time_stmt in node.body:
                        break
                    # print("yes, it is a call node: ", ast.unparse(child))

                    index = node.body.index(child)
                    # node.body.remove(child)
                    node.body.insert(index, self.print_total_stmt_pythonic)
                    node.body.insert(index, self.diff_time_stmt)
                    node.body.insert(index, self.end_time_stmt)
                    node.body.insert(index, self.new_node_simple)
                    node.body.insert(index, self.start_time_stmt)
                    node.body.insert(index, self.import_time_stmt)

                    self.flag = 1
                    break

                node.body[ind] = self.generic_visit(child)
        if hasattr(node, "orelse") and not self.flag:
            # print("come here: ",ast.unparse(node))
            for ind, child in enumerate(node.orelse):
                try:
                    if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):
                        if self.import_time_stmt in node.orelse:
                            break


                        index = node.orelse.index(child)
                        # node.orelse.remove(child)
                        node.orelse.insert(index, self.print_total_stmt_pythonic)
                        node.orelse.insert(index, self.diff_time_stmt)
                        node.orelse.insert(index, self.end_time_stmt)
                        node.orelse.insert(index, self.new_node_simple)
                        node.orelse.insert(index, self.start_time_stmt)
                        node.orelse.insert(index, self.import_time_stmt)
                        self.flag = 1
                        break
                    node.orelse[ind] = self.generic_visit(child)
                except:
                    traceback.print_exc()
        return node
class Rewrite_insert_time(ast.NodeTransformer):
    def __init__(self,node,new_node,node_simple,new_node_simple):
        self.old_node =node
        self.new_node =new_node
        self.old_node_simple = node_simple
        self.new_node_simple = new_node_simple
        TimerStmt.__init__(self)
        self.flag=0


    def generic_visit(self, node):
        if hasattr(node, "body"):
            # print("node: ",ast.unparse(node))
            ass_re = None
            for ind, child in enumerate(node.body):
                if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):

                    if self.import_time_stmt in node.body:
                        break
                    # end_lineno = child.end_lineno
                    index = node.body.index(child)

                    node.body.insert(index, self.print_total_stmt)
                    node.body.insert(index, self.diff_time_stmt)
                    node.body.insert(index, self.end_time_stmt)
                    node.body.insert(index, self.old_node_simple)
                    node.body.insert(index, self.start_time_stmt)
                    node.body.insert(index, self.import_time_stmt)


                    self.flag = 1
                    break

                node.body[ind] = self.generic_visit(child)
        if hasattr(node, "orelse") and not self.flag:
            # print("come here: ",ast.unparse(node))
            for ind, child in enumerate(node.orelse):
                try:
                    if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):
                        if self.import_time_stmt in node.orelse:
                            break
                        # end_lineno=child.end_lineno

                        index = node.orelse.index(child)
                        node.orelse.insert(index, self.print_total_stmt)
                        node.orelse.insert(index, self.diff_time_stmt)
                        node.orelse.insert(index, self.end_time_stmt)
                        node.orelse.insert(index, self.old_node_simple)
                        node.orelse.insert(index, self.start_time_stmt)
                        node.orelse.insert(index, self.import_time_stmt)
                        # print("yes, it is a call node: ", ast.unparse(child))

                        break
                    node.orelse[ind] = self.generic_visit(child)
                except:
                    traceback.print_exc()
        return node

class Rewrite_insert_time_add_len_unpack(ast.NodeTransformer):
    def __init__(self,node,new_node,node_simple,new_node_simple):
        self.old_node =node
        self.new_node =new_node
        self.old_node_simple = node_simple
        self.new_node_simple = new_node_simple
        TimerStmt.__init__(self)
        self.flag=0
        var = ast.unparse(self.old_node.iter)
        print_len_stmt = f"try:\n    print('len: ',len({var}[0]))\nexcept:\n    print('len: ',0)"

        for e in ast.walk(ast.parse(print_len_stmt)):
            if isinstance(e, ast.stmt):
                self.print_len_stmt_node = e
                break


    def generic_visit(self, node):
        if hasattr(node, "body"):
            # print("node: ",ast.unparse(node))
            ass_re = None
            for ind, child in enumerate(node.body):
                if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):

                    if self.import_time_stmt in node.body:
                        break
                    # end_lineno = child.end_lineno
                    index = node.body.index(child)
                    node.body.insert(index, self.print_len_stmt_node)
                    node.body.insert(index, self.print_total_stmt)
                    node.body.insert(index, self.diff_time_stmt)
                    node.body.insert(index, self.end_time_stmt)
                    node.body.insert(index, self.old_node_simple)
                    node.body.insert(index, self.start_time_stmt)
                    node.body.insert(index, self.import_time_stmt)


                    self.flag = 1
                    break

                node.body[ind] = self.generic_visit(child)
        if hasattr(node, "orelse") and not self.flag:
            # print("come here: ",ast.unparse(node))
            for ind, child in enumerate(node.orelse):
                try:
                    if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):
                        if self.import_time_stmt in node.orelse:
                            break
                        # end_lineno=child.end_lineno

                        index = node.orelse.index(child)
                        node.body.insert(index, self.print_len_stmt_node)
                        node.orelse.insert(index, self.print_total_stmt)
                        node.orelse.insert(index, self.diff_time_stmt)
                        node.orelse.insert(index, self.end_time_stmt)
                        node.orelse.insert(index, self.old_node_simple)
                        node.orelse.insert(index, self.start_time_stmt)
                        node.orelse.insert(index, self.import_time_stmt)
                        # print("yes, it is a call node: ", ast.unparse(child))

                        break
                    node.orelse[ind] = self.generic_visit(child)
                except:
                    traceback.print_exc()
        return node

class Rewrite_insert_time_add_len(ast.NodeTransformer):
    def __init__(self,node,new_node,node_simple,new_node_simple):
        self.old_node =node
        self.new_node =new_node
        self.old_node_simple = node_simple
        self.new_node_simple = new_node_simple
        TimerStmt.__init__(self)
        self.flag=0


    def generic_visit(self, node):
        if hasattr(node, "body"):
            # print("node: ",ast.unparse(node))
            ass_re = None
            for ind, child in enumerate(node.body):
                if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):

                    if self.import_time_stmt in node.body:
                        break
                    # end_lineno = child.end_lineno
                    index = node.body.index(child)
                    var = ast.unparse(self.old_node_simple.iter)
                    print_len_stmt = f"print('len: ',len({var}))"
                    for e in ast.walk(ast.parse(print_len_stmt)):
                        if isinstance(e, ast.stmt):
                            node.body.insert(index, e)
                            break
                    node.body.insert(index, self.print_total_stmt)
                    node.body.insert(index, self.diff_time_stmt)
                    node.body.insert(index, self.end_time_stmt)
                    node.body.insert(index, self.old_node_simple)
                    node.body.insert(index, self.start_time_stmt)
                    node.body.insert(index, self.import_time_stmt)


                    self.flag = 1
                    break

                node.body[ind] = self.generic_visit(child)
        if hasattr(node, "orelse") and not self.flag:
            # print("come here: ",ast.unparse(node))
            for ind, child in enumerate(node.orelse):
                try:
                    if child.lineno == self.old_node.lineno and ast.unparse(child) == ast.unparse(self.old_node):  # and ast.unparse(child)==ast.unparse(self.call_node):
                        if self.import_time_stmt in node.orelse:
                            break
                        # end_lineno=child.end_lineno

                        index = node.orelse.index(child)
                        var = ast.unparse(self.old_node_simple.iter)
                        print_len_stmt = f"print('len: ',len({var}))"
                        for e in ast.walk(ast.parse(print_len_stmt)):
                            if isinstance(e, ast.stmt):
                                node.body.insert(index, e)
                                break
                        node.orelse.insert(index, self.print_total_stmt)
                        node.orelse.insert(index, self.diff_time_stmt)
                        node.orelse.insert(index, self.end_time_stmt)
                        node.orelse.insert(index, self.old_node_simple)
                        node.orelse.insert(index, self.start_time_stmt)
                        node.orelse.insert(index, self.import_time_stmt)
                        # print("yes, it is a call node: ", ast.unparse(child))

                        break
                    node.orelse[ind] = self.generic_visit(child)
                except:
                    traceback.print_exc()
        return node
# class Rewrite(ast.NodeTransformer):
#     def __init__(self,node,new_node):
#         self.old_node =node
#         self.new_node =new_node
#
#     def generic_visit(self, node):
#         if hasattr(node, "body"):
#             if isinstance(node,ast.For):
#                 print("come here: ", ast.unparse(node), ast.unparse(self.old_node))
#             if hasattr(node,"lineno"):
#                 if  node.lineno==self.old_node.lineno:
#                     print("come here: ", ast.unparse(node),ast.unparse(self.old_node))
#                 if node.lineno==self.old_node.lineno and ast.unparse(node)==ast.unparse(self.old_node):
#                     print("come here")
#                     return self.new_node
#
#             for ind,child in enumerate(node.body):
#                     node.body[ind] = self.generic_visit(node.body[ind])
#         return node

class Rewrite_boolop(ast.NodeTransformer):
    def __init__(self,old_node,new_node):
        self.old_node =old_node
        self.new_node =new_node
        self.modify_flag=0
    def visit_BoolOp(self, node):

        if ast.unparse(node) == ast.unparse(self.old_node) and self.old_node.lineno == node.lineno:
            # print("***********come here",ast.unparse(arg))
            self.modify_flag=1
            return self.new_node
        for ind,value in enumerate(node.values):
            node.values[ind]=self.visit(value)
        return node

def replace_content_var_unpack_for_target_insert_time(file_path,old_tree,new_tree,old_tree_simple,new_tree_simple,me_name):
    content = util.load_file_path(file_path)
    all_tree = ast.parse(content)
    old_tree_str=ast.unparse(all_tree)
    rew = Rewrite_insert_time(old_tree, new_tree,old_tree_simple,new_tree_simple)
    all_tree = rew.visit(all_tree)
    flag_same=old_tree_str == ast.unparse(all_tree)
    print("whether code1 same: ",old_tree_str==ast.unparse(all_tree))
    ana_py = ast_performance_util.Fun_Analyzer_Insert_Stmt(me_name)
    all_tree = ana_py.visit(all_tree)
    return content, ast.unparse(all_tree),flag_same
def replace_content_var_unpack_for_target_insert_time_add_len_unpack(file_path,old_tree,new_tree,old_tree_simple,new_tree_simple,me_name):
    content = util.load_file_path(file_path)
    all_tree = ast.parse(content)
    old_tree_str=ast.unparse(all_tree)
    rew = Rewrite_insert_time_add_len_unpack(old_tree, new_tree,old_tree_simple,new_tree_simple)
    all_tree = rew.visit(all_tree)
    flag_same=old_tree_str == ast.unparse(all_tree)
    print("whether code1 same: ",old_tree_str==ast.unparse(all_tree))
    ana_py = ast_performance_util.Fun_Analyzer_Insert_Stmt(me_name)
    all_tree = ana_py.visit(all_tree)
    return content, ast.unparse(all_tree),flag_same
def replace_content_var_unpack_for_target_insert_time_add_size(file_path,old_tree,new_tree,old_tree_simple,new_tree_simple,me_name):
    content = util.load_file_path(file_path)
    all_tree = ast.parse(content)
    old_tree_str=ast.unparse(all_tree)
    rew = Rewrite_insert_time_add_len(old_tree, new_tree,old_tree_simple,new_tree_simple)
    all_tree = rew.visit(all_tree)
    flag_same=old_tree_str == ast.unparse(all_tree)
    print("whether code1 same: ",old_tree_str==ast.unparse(all_tree))
    ana_py = ast_performance_util.Fun_Analyzer_Insert_Stmt(me_name)
    all_tree = ana_py.visit(all_tree)
    return content, ast.unparse(all_tree),flag_same
def replace_content_var_unpack_for_target(file_path,old_tree,new_tree,old_tree_simple,new_tree_simple,me_name):
    content = util.load_file_path(file_path)
    all_tree = ast.parse(content)
    old_tree_str=ast.unparse(all_tree)
    rew = Rewrite(old_tree, new_tree,old_tree_simple,new_tree_simple)
    all_tree = rew.visit(all_tree)
    flag_same=old_tree_str == ast.unparse(all_tree)
    print("whether code1 same: ",old_tree_str==ast.unparse(all_tree))
    ana_py = ast_performance_util.Fun_Analyzer_Insert_Stmt(me_name)
    all_tree = ana_py.visit(all_tree)
    return content, ast.unparse(all_tree),flag_same
def replace_content_var_unpack_for_target_add_unpack_Starred(file_path,old_tree,new_tree,old_tree_simple,new_tree_simple,me_name):
    content = util.load_file_path(file_path)
    all_tree = ast.parse(content)
    old_tree_str=ast.unparse(all_tree)
    rew = Rewrite(old_tree, new_tree,old_tree_simple,new_tree_simple)
    all_tree = rew.visit(all_tree)
    flag_same=old_tree_str == ast.unparse(all_tree)
    print("whether code1 same: ",old_tree_str==ast.unparse(all_tree))
    ana_py = ast_performance_util.Fun_Analyzer_Insert_Stmt(me_name)
    all_tree = ana_py.visit(all_tree)
    return content, ast.unparse(all_tree),flag_same

def replace_content_var_unpack_for_target_insert_time_simple(file_path, old_tree, new_tree):
        content = util.load_file_path(file_path)
        all_tree = ast.parse(content)
        old_tree_str = ast.unparse(all_tree)
        rew = Rewrite_insert_time(old_tree, new_tree)
        all_tree = rew.visit(all_tree)
        flag_same = old_tree_str == ast.unparse(all_tree)
        print("whether code1 same: ", old_tree_str == ast.unparse(all_tree))
        # ana_py = ast_performance_util.Fun_Analyzer_Insert_Stmt(me_name)
        # all_tree = ana_py.visit(all_tree)
        return content, ast.unparse(all_tree), flag_same

def replace_content_var_unpack_for_target_simple(file_path, old_tree, new_tree):
        content = util.load_file_path(file_path)
        all_tree = ast.parse(content)
        old_tree_str = ast.unparse(all_tree)
        rew = Rewrite(old_tree, new_tree)
        all_tree = rew.visit(all_tree)
        flag_same = old_tree_str == ast.unparse(all_tree)
        print("whether code1 same: ", old_tree_str == ast.unparse(all_tree))
        # ana_py = ast_performance_util.Fun_Analyzer_Insert_Stmt(me_name)
        # all_tree = ana_py.visit(all_tree)
        return content, ast.unparse(all_tree), flag_same
    # res_copy = content.split("\n")
    # beg = compl_node.lineno
    # end = compl_node.end_lineno
    # # print("beg,end: ",beg,end)
    # indent = ""
    # for ind, e in enumerate(res_copy[beg - 1]):
    #     if e != " ":
    #         indent = " " * ind
    #         break
    # # res_copy[beg - 1] = [indent +e for e in ast.unparse(sim_node).split("\n")]
    # res_copy[beg - 1:end] = [indent +e for e in ast.unparse(sim_node).split("\n")]
    #
    # return content, "\n".join(res_copy)



if __name__ == '__main__':
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    # save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_else/"
    '''
    complic_code_me_info_dir_pkl 
    {key repo_name: {
        key full_me_id: {
            file_html:  xx
            file_path: xx
            me_line_no: [{new_file_code: xx

            old_fragm_code_line:xx
            new_frgam_code_line:xx}, {...}]
        }   
    }
    complic_code_me_overload_info_dir_pkl
    {key repo_name: {
        key full_me_id: {
            file_html:  xx
            file_path: xx
            me_line_no: [
                {new_file_code: xx, old_fragm_code_line:xx, new_frgam_code_line:xx}, {...}],
            me_line_no:[]
        }  
    }
    '''
    complicated_code_dir_pkl=util.data_root + "transform_complicate_to_simple_pkl/for_compre_dict/"

    # complicated_code_dir_pkl=util.data_root + "transform_complicate_to_simple_pkl/for_compre_set/"
    complicated_code_dir_pkl= util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated/"
    # complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/chain_comparison/"
    # complicated_code_dir_pkl=util.data_root +"transform_complicate_to_simple_pkl/var_unpack_call_star_complicated/"
    complicated_code_dir_pkl=util.data_root +"transform_complicate_to_simple_pkl/var_unpack_for_target_complicated/"
    # complicated_code_dir_pkl=util.data_root + "transform_complicate_to_simple_pkl/multip_assign_complicated/"
    # complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_else/"
    # complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_list/"

    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/for_compre_set/"#for_else
    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/truth_value_test_complicated/"#for_else
    # complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/chain_comparison/"#for_else
    # complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/var_unpack_call_star_complicated/"#for_else
    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/var_unpack_for_target_complicated/"#for_else
    # complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/multip_assign_complicated/"#for_else
    # complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/for_else/"#for_else
    # complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl_test/each_idiom_type_all_methods/for_compre_list/"#for_else
    # complic_code_me_info_dir_pkl_test= util.data_root
    # dict_repo_file_python = util.load_json(util.data_root, "jupyter3_repos_files_info")

    repo_list = []
    count_file = 0
    dict_repo_need_test_me = dict()
    dict_repo_need_test_me_overload = dict()
    result_me_info = []
#/mnt/zejun/smp/data/python_star_2000repo/nni/nni/algorithms/hpo/curvefitting_assessor/model_factory_copy_zejun.py
    for repo_name in dict_repo_file_python:
        if repo_name !="mlens":#"nibabel":#"mlens":#"pingouin":#"thunder":#"pingouin":#"mlens":#"patroni":#"cloud-custodian":# "sacred":#"docker-py":#"mitmproxy":#
            continue
        dict_repo_need_test_me[repo_name] = dict()
        dict_repo_need_test_me_overload[repo_name] = dict()
        if not os.path.exists(complicated_code_dir_pkl+repo_name+".pkl"):
            continue
        complicate_code = util.load_pkl(complicated_code_dir_pkl, repo_name)
        for file_html in complicate_code:
            #come the file_html:  https://github.com/caronc/apprise/tree/master/apprise/AppriseAttachment.py
#come the file_html:  https://github.com/pymc-devs/pymc/tree/master/pymc/sampling.py
#>>>>>>>>>>dict_me_re:  ['pymc.tests.test_step.TestDEMetropolisZ.test_tuning_reset'] 1>>>>>>>>>>dict_me_re:  [] 0
#https://github.com/coursera-dl/coursera-dl/tree/master/coursera/filtering.py
#https://github.com/Chia-Network/chia-blockchain/tree/master/chia/util/bech32m.py
#https://github.com/Chia-Network/chia-blockchain/tree/master/chia/util/type_checking.py
#https://github.com/kivy/python-for-android/tree/master/pythonforandroid/pythonpackage.py
            #https://github.com/aws/aws-cli/tree/master/awscli/customizations/s3/subcommands.py 这个是没有通过测试用例
            #https://github.com/pytransitions/transitions/tree/master/transitions/extensions/nesting.py 这个是没有通过测试用例
            #https://github.com/ytdl-org/youtube-dl/tree/master/youtube_dl/utils.py 这个是没有通过测试用例
            #https://github.com/sympy/sympy/tree/master/sympy/crypto/crypto.py 这个是没有通过测试用例
            #https://github.com/localstack/localstack/tree/master/localstack/services/sns/sns_listener.py 这个是code没有改变
            # if file_html != "https://github.com/pymc-devs/pymc/tree/master/pymc/sampling.py":#"https://github.com/networkx/networkx/tree/master/networkx/algorithms/connectivity/kcomponents.py":#"https://github.com/IDSIA/sacred/tree/master/sacred/observers/mongo.py":#"https://github.com/cloud-custodian/cloud-custodian/tree/master/c7n/provider.py":#"https://github.com/networkx/networkx/tree/master/networkx/generators/joint_degree_seq.py":#"https://github.com/bndr/pipreqs/tree/master/pipreqs/pipreqs.py":#"https://github.com/amperser/proselint/tree/master/proselint/tools.py":#"https://github.com/networkx/networkx/tree/master/networkx/readwrite/json_graph/adjacency.py":##"https://github.com/microsoft/nni/tree/master/nni/tools/nnictl/nnictl_utils.py":#"https://github.com/networkx/networkx/tree/master/networkx/readwrite/json_graph/adjacency.py":#"https://github.com/amperser/proselint/tree/master/proselint/tools.py":#"https://github.com/aws/aws-cli/tree/master/awscli/customizations/s3/subcommands.py":#"https://github.com/nccgroup/ScoutSuite/tree/master/ScoutSuite/providers/aws/utils.py":#"https://github.com/microsoft/nni/tree/master/nni/algorithms/hpo/networkmorphism_tuner/graph_transformer.py":#"https://github.com/localstack/localstack/tree/master/localstack/services/awslambda/lambda_api.py":#"https://github.com/localstack/localstack/tree/master/localstack/utils/common.py":#"https://github.com/aws/aws-cli/tree/master/awscli/compat.py":#"https://github.com/spulec/moto/tree/master/moto/config/models.py":#"https://github.com/cookiecutter/cookiecutter/tree/master/cookiecutter/hooks.py":#"https://github.com/yt-dlp/yt-dlp/tree/master/yt_dlp/utils.py":#"https://github.com/ytdl-org/youtube-dl/tree/master/youtube_dl/utils.py":#"https://github.com/OmkarPathak/pygorithm/tree/master/pygorithm/greedy_algorithm/fractional_knapsack.py":#"https://github.com/OmkarPathak/pygorithm/tree/master/pygorithm/strings/anagram.py":#"https://github.com/amperser/proselint/tree/master/proselint/tools.py":#"https://github.com/cloudtools/troposphere/tree/master/troposphere/validators.py":#"https://github.com/pytransitions/transitions/tree/master/transitions/extensions/nesting.py":#"https://github.com/ytdl-org/youtube-dl/tree/master/youtube_dl/utils.py":#"https://github.com/microsoft/nni/tree/master/nni/algorithms/hpo/networkmorphism_tuner/graph_transformer.py":#"https://github.com/amperser/proselint/tree/master/proselint/tools.py":#"https://github.com/sympy/sympy/tree/master/sympy/crypto/crypto.py":#"https://github.com/ytdl-org/youtube-dl/tree/master/youtube_dl/utils.py":#"https://github.com/sympy/sympy/tree/master/sympy/crypto/crypto.py":#"https://github.com/yt-dlp/yt-dlp/tree/master/yt_dlp/utils.py":#"https://github.com/amperser/proselint/tree/master/proselint/tools.py":#"https://github.com/pytransitions/transitions/tree/master/transitions/extensions/nesting.py":#"https://github.com/microsoft/nni/tree/master/nni/algorithms/hpo/networkmorphism_tuner/graph_transformer.py":  # "https://github.com/pymc-devs/pymc/tree/master/pymc/sampling.py":#"https://github.com/smicallef/spiderfoot/tree/master//sflib.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#
            #     continue
            #https://github.com/threat9/routersploit/tree/master/routersploit/modules/exploits/routers/billion/billion_5200w_rce.py
            #https://github.com/google/clusterfuzz/tree/master/src/clusterfuzz/_internal/metrics/logs.py
            # if file_html=="https://github.com/google/clusterfuzz/tree/master/src/clusterfuzz/_internal/metrics/logs.py":
            #https://github.com/bndr/pipreqs/tree/master/pipreqs/pipreqs.py
            #https://github.com/smicallef/spiderfoot/tree/master//sflib.py
            # if file_html!="https://github.com/smicallef/spiderfoot/tree/master/spiderfoot/helpers.py":#"https://github.com/threat9/routersploit/tree/master/routersploit/modules/exploits/routers/billion/billion_5200w_rce.py":#"https://github.com/google/clusterfuzz/tree/master/src/clusterfuzz/_internal/metrics/logs.py":#"https://github.com/threat9/routersploit/tree/master/routersploit/modules/exploits/routers/technicolor/tg784_authbypass.py":#"https://github.com/microsoft/nni/tree/master/nni/algorithms/hpo/hyperopt_tuner.py":#"https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python/tests/conjecture/test_engine.py":
            #     continue
            if file_html!="https://github.com/flennerhag/mlens/tree/master/mlens/config.py":#"https://github.com/nipy/nibabel/tree/master/nibabel/fileslice.py":#"https://github.com/flennerhag/mlens/tree/master/mlens/config.py":#"https://github.com/raphaelvallat/pingouin/tree/master/pingouin/regression.py":#"https://github.com/thunder-project/thunder/tree/master/thunder/series/readers.py":#"https://github.com/flennerhag/mlens/tree/master/mlens/config.py":#"https://github.com/zalando/patroni/tree/master/patroni/log.py":#"https://github.com/cloud-custodian/cloud-custodian/tree/master/c7n/schema.py":#"https://github.com/IDSIA/sacred/tree/master/sacred/observers/tinydb_hashfs/tinydb_hashfs.py":#"https://github.com/docker/docker-py/tree/master/docker/models/services.py":#"https://github.com/cloud-custodian/cloud-custodian/tree/master/c7n/schema.py":#"https://github.com/mitmproxy/mitmproxy/tree/master/mitmproxy/net/http/url.py":#"https://github.com/nccgroup/ScoutSuite/tree/master/ScoutSuite/core/console.py":#"https://github.com/facebookresearch/hydra/tree/master/hydra/_internal/utils.py":#"https://github.com/threat9/routersploit/tree/master/routersploit/modules/exploits/routers/bhu/bhu_urouter_rce.py":#"https://github.com/falconry/falcon/tree/master/falcon/util/sync.py":#"https://github.com/pytoolz/toolz/tree/master/toolz/functoolz.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#"https://github.com/cloud-custodian/cloud-custodian/tree/master/c7n/provider.py":#"https://github.com/huggingface/transformers/tree/master/src/transformers/image_utils.py":#"https://github.com/huggingface/transformers/tree/master/src/transformers/trainer_pt_utils.py":#"https://github.com/yt-dlp/yt-dlp/tree/master/yt_dlp/utils.py":#"https://github.com/bottlepy/bottle/tree/master//bottle.py":#"https://github.com/psf/requests/tree/master/requests/cookies.py":#"https://github.com/pytransitions/transitions/tree/master/transitions/core.py":#"https://github.com/zalando/patroni/tree/master/patroni/ctl.py":#"https://github.com/google/yapf/tree/master/yapf/yapflib/file_resources.py":#
                continue
            real_file_html = file_html.replace("//", "/")
            #
            # packa_pre=".".join(real_file_html.split("/")[6:])[:-3]
            rela_path = "/".join(real_file_html.split("/")[6:])
            file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
            print("file_html: ", file_html, file_path)
            content = util.load_file_path(file_path)
            with open(file_path, "r") as f:

                res = f.readlines()  # res 为列表

            for cl in complicate_code[file_html]:
                class_name = cl
                print("class name: ", cl)
                for me in complicate_code[file_html][cl]:
                    # me_name=me.split("$")[0]
                    # line_beg=me.split("$")[1]
                    if complicate_code[file_html][cl][me]:
                        for ind, (old_tree,new_tree) in enumerate(complicate_code[file_html][cl][me]):
                            old_tree_str = ast.unparse(old_tree)
                            # if " None" in old_tree_str or " True" in old_tree_str:
                            #     continue
                            print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ", ast.unparse(new_tree))  #
                            print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ",old_tree.lineno,ast.unparse(old_tree) )  # old_tree.lineno,

                            #old_tree, ass,new_tree;  old_tree, new_tree;(arg_list, new_tree ) each_assign_list, new_tree, old_tree, new_tree,break_list_in_for
                        # for ind, (arg_list, new_tree ) in enumerate(complicate_code[file_html][cl][me]):
                        # for ind, (each_assign_list, new_tree_content) in enumerate(complicate_code[file_html][cl][me]):
                        # for ind, (for_node, assign_node,remove_ass_flag,new_tree) in enumerate(complicate_code[file_html][cl][me]):
                        # for ind, (old_tree, new_tree,break_list_in_for) in enumerate(complicate_code[file_html][cl][me]):
                            # old_tree=arg_list
                            # print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ",  ast.unparse(new_tree))#
                            # print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ",for_node.lineno,ast.unparse(assign_node),ast.unparse(for_node) )  # old_tree.lineno,

                            # print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ",  ast.unparse(new_tree))#
                            # print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ",old_tree.lineno,ast.unparse(old_tree))#old_tree.lineno,arg_list
                            # for child in ast.walk(ast.parse(new_tree_content)):
                            #     if isinstance(child,ast.Assign):
                            #         new_tree=child
                            #         break
                            # for each_ass in each_assign_list:
                            #     print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ", ast.unparse(each_ass),each_ass.lineno)#old_tree.lineno,
                            # print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ",ast.unparse(new_tree))#ast.unparse(new_tree))#old_tree.lineno,arg_list

                        # print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ", ast.unparse(old_tree))#old_tree.lineno,
                        #     old_content,new_content,flag_same=replace_file_content_for_compre_3_category(repo_name,file_html,for_node, assign_node,new_tree,remove_ass_flag)
                        #     old_content, new_content,flag_same = replace_content_chain_compar(repo_name, file_html,old_tree,new_tree)
                            old_content, new_content, flag_same =replace_content_var_unpack_for_target(repo_name,file_html,old_tree,new_tree)
                            # old_content,new_content,flag_same=replace_content_truth_value_test(repo_name,file_html,old_tree,new_tree)
                            # arg_seq=arg_list[0]
                            # call_node=arg_list[-2]
                            # print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ",ast.unparse(arg_seq[0]),
                            #   arg_seq[0].lineno,ast.unparse(call_node),call_node.lineno)  # old_tree.lineno,arg_list

                            # old_content,new_content,flag_same=replace_content_chain_compar(repo_name,file_html,old_tree,new_tree)
                        #     old_content,new_content=replace_content_var_unpack_call_star(repo_name,file_html,arg_seq,new_tree,call_node)
                            # old_content,new_content=replace_content_var_unpack_for_target(repo_name,file_html,old_tree,new_tree)
                            # old_content,new_content,flag_same=replace_content_multi_ass(repo_name,file_html,each_assign_list,new_tree)
                            # old_content,new_content=replace_content_for_else(repo_name,file_html,old_tree,new_tree)
                            if flag_same:
                                break
                            util.save_file(complic_code_me_info_dir_pkl_test, "test", new_content, ".txt", "w")
                            util.save_file(complic_code_me_info_dir_pkl_test, "test_old", old_content, ".txt", "w")
                            print(">>>>>>>>>>>>>>>>>>>>new file:\n ", flag_same,new_content)
                            print(">>>>>>>>>>>>>>>>>>>>old file:\n ", old_content)
                            # break
                        # for ind, (old_tree, new_tree, break_list_info) in enumerate(complicate_code[file_html][cl][me]):
                        #     print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ", new_tree.lineno, ast.unparse(new_tree))
                        #     print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ", old_tree.lineno, ast.unparse(old_tree))
                        #     replace_file_content_for_compre_3_category(repo_name,file_html,)
                        #     util.save_file(complic_code_me_info_dir_pkl_test, "test", "\n".join(res_copy), ".txt", "w")
                        #     util.save_file(complic_code_me_info_dir_pkl_test, "test_old", content, ".txt", "w")
                        #     print(">>>>>>>>>>>>>>>>>>>>new file:\n ", "\n".join(res_copy))
                        #     print(">>>>>>>>>>>>>>>>>>>>old file:\n ", content)

                        else:
                            continue
                        break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            continue
        break


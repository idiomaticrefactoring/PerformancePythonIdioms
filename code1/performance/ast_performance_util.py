import ast
import copy

Keywords=["False",      "await",      "else",       "import",     "pass",
"None",       "break",      "except",     "in",         "raise",
"True",       "class",      "finally",    "is",         "return",
"and",        "continue",   "for",        "lambda",     "try",
"as",         "def",        "from",       "nonlocal",   "while",
"assert",     "del",       "global",     "not",        "with",
"async",      "elif",       "if",         "or",         "yield"]
class Fun_Analyzer(ast.NodeTransformer):
    def __init__(self,me_name="",iterations=10):
        self.func_def_list = []
        self.me_name = me_name
        self.flag=0
        self.iterations=iterations
    def visit_FunctionDef(self, node):
        if node.name==self.me_name:
            para = "pytest.mark.parametrize('execution_number', range(2))"
            for a_node in ast.walk(ast.parse(para)):
                if isinstance(a_node, ast.Call):
                    para_node = a_node
                    break
            # node
            print("para_node: ",para_node)
            # setattr(node,"decorator_list",[para_node])
            node.decorator_list=[]
            node.decorator_list.append(para_node)
            # a = f"import gc\nfor i in range({self.iterations}):\n    print('>>>>>>>>>>>>>>>>>>>>>>>')"
            # gc="gc.collect()"
            # gc_import="import gc"
            # for a_node in ast.walk(ast.parse(gc)):
            #     if isinstance(a_node, ast.stmt):
            #         gc_node=a_node
            #         break
            # for a_node in ast.walk(ast.parse(gc_import)):
            #     if isinstance(a_node, ast.Import):
            #         gc_import_node=a_node
            #         break
            # tree_a = ast.parse(a)
            # for a_node in ast.walk(tree_a):
            #     if isinstance(a_node, ast.For):
            #         pos=len(node.body)
            #         node.body.insert(pos,gc_node)
            #         node.body.insert(pos, gc_import_node)
            #         a_node.body = node.body
            #         node.body = [a_node]
            #         self.flag=1
            #         break
            self.flag = 1
            return node
        else:
            ast.NodeVisitor.generic_visit(self, node)
            return node



    def visit_ClassDef(self, node):
        stmt="import pytest"
        for a_node in ast.walk(ast.parse(stmt)):
            if isinstance(a_node, ast.Import):
                    import_node=a_node
                    break
        class_ana=Fun_Analyzer(self.me_name,self.iterations)
        for ind,stmt in enumerate(node.body):
            class_ana.visit(stmt)

            if class_ana.flag:
                node.body.insert(ind, import_node)
                break
                # node.body.insert(para_node)

        self.flag=class_ana.flag
        return node
class Fun_Analyzer_Insert_Stmt(ast.NodeTransformer):
    def __init__(self,me_name=""):
        self.func_def_list = []
        self.me_name = me_name
        self.flag=0
    def visit_FunctionDef(self, node):
        # print(">>>>>>visit method name>>>>>>>>: ",node.name)
        if node.name==self.me_name:
            # print(">>>>>>visit_FunctionDef>>>>>>>>")
            para = "print('\\n>>>>>>>>Come tested method zejun')"
            for a_node in ast.walk(ast.parse(para)):
                if isinstance(a_node, ast.stmt):
                    node.body.insert(0,a_node)
                    break
            self.flag = 1
            return node
        else:
            # print(">>>>>>>>>here you are")
            ast.NodeTransformer.generic_visit(self, node)
            return node



    def visit_ClassDef(self, node):
        # print(">>>>>>>come visit_ClassDef: ",node.name)
        class_ana=Fun_Analyzer_Insert_Stmt(self.me_name)
        for ind,stmt in enumerate(node.body):
            class_ana.visit(stmt)

            if class_ana.flag:
                # node.body.insert(ind, import_node)
                break
        # class_ana.visit(node)
        self.flag=class_ana.flag
        return node
    # def generic_visit(self, node):
    #     ast.NodeVisitor.generic_visit(self, node)
class Rewrite_call(ast.NodeTransformer):
    def __init__(self,me_name):
        self.me_name =me_name
        self.contain_flag=0

    def generic_visit(self, node):
        for e in ast.walk(node):
            if isinstance(e,ast.Call):
                fun_node=e.func
                if self.me_name in ast.unparse(fun_node):
                    self.contain_flag=1
                    break

        return node
class Fun_Analyzer_Add_Time(ast.NodeTransformer):
    def __init__(self,me_name="",target_me_name="",iterations=10):
        self.func_def_list = []
        self.me_name = me_name
        self.target_me_name=target_me_name
        self.flag=0
        self.iterations=iterations
        self.print_total_stmt = 'print("\\n************it is method************\\n")'

        for node in ast.walk(ast.parse(self.print_total_stmt)):
            if isinstance(node, (ast.stmt)):
                self.print_total_stmt = node
                break

    def visit_FunctionDef(self, node):
        if node.name==self.me_name:
            # para = "pytest.mark.parametrize('execution_number', range(2))"
            # for a_node in ast.walk(ast.parse(para)):
            #     if isinstance(a_node, ast.Call):
            #         para_node = a_node
            #         break
            # # node
            # # print("para_node: ",para_node)
            # # setattr(node,"decorator_list",[para_node])
            # node.decorator_list=[]
            # node.decorator_list.append(para_node)

            new_node=copy.deepcopy(node)
            bias=0
            for ind,stmt in enumerate(node.body):
                re_call = Rewrite_call(self.target_me_name)
                stmt = re_call.visit(stmt)
                # print("come here")
                if re_call.contain_flag:
                    # print("come here")
                    new_node.body.insert(ind+bias,self.print_total_stmt)
                bias += re_call.contain_flag
            self.flag = 1
            return new_node
        else:
            ast.NodeVisitor.generic_visit(self, node)
            return node



    def visit_ClassDef(self, node):
        stmt="import pytest"
        for a_node in ast.walk(ast.parse(stmt)):
            if isinstance(a_node, ast.Import):
                    import_node=a_node
                    break
        class_ana=Fun_Analyzer(self.me_name,self.iterations)
        for ind,stmt in enumerate(node.body):
            class_ana.visit(stmt)

            if class_ana.flag:
                node.body.insert(ind, import_node)
                break
                # node.body.insert(para_node)

        self.flag=class_ana.flag
        return node
class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.func_def_list = []

    def visit_FunctionDef(self,node):
        self.func_def_list.append(node)
    def visit_If(self, node: ast.If):
        if ast.unparse(node.test)=="__name__ == '__main__'":
            self.func_def_list.append(node)
def set_dict_class_code_list(tree,dict_class,class_name,new_code_list):
    me_name = tree.name if hasattr(tree, "name") else "if_main_my"
    me_lineno = tree.lineno
    me_id = "".join([me_name, "$", str(me_lineno)])

    if class_name not in dict_class:
        dict_class[class_name] = dict()
        dict_class[class_name][me_id] = new_code_list
    else:

        dict_class[class_name][me_id] = new_code_list

def get_basic_count(e):

    count=0
    # print("e dict: ",e.__dict__)
    if isinstance(e, (ast.Tuple,ast.List)):
        # count += len(e.elts)
        for cur in e.elts:
            count +=get_basic_count(cur)

    else:
        # print(e.__dict__, " are not been parsed")
        count +=1


    return count
def get_basic_object(e,var_list=[]):
    if isinstance(e, (ast.Tuple,ast.List)):
        # count += len(e.elts)
        for cur in e.elts:
            get_basic_object(cur,var_list)

    else:
        # print(e.__dict__, " are not been parsed")
        var_list.append(ast.unparse(e))


def extract_ast_block_node(node,node_list):
    for k in node._fields:

        v = getattr(node, k)

        if isinstance(v, list):
            # print("come here", v)
            a=[]
            for e in v:
                a.append(e)
                if isinstance(e, ast.AST):
                    extract_ast_block_node(e, node_list)
            node_list.append(a)
        elif isinstance(v, ast.AST):
            # print("come here", v.__dict__)
            if v._fields:
                extract_ast_block_node(v,node_list)
def extract_ast_cur_layer_node(node,node_list):
    # if node._fields:
    #     node_list.append(list(node._fields))
    for k in node._fields:
        v = getattr(node, k)

        if isinstance(v, list):
            a = []
            for e in v:
                a.append(e)
            node_list.append(a)
            for e in v:
                if e._fields:
                    extract_ast_block_node(e, node_list)


        elif isinstance(v, ast.AST):
            if v._fields:
                extract_ast_block_node(v, node_list)

if __name__ == '__main__':
    code='''
a.b=2
if label_names:
    a=2
    num_tensors_in_label = len(label_names)
else:
    num_tensors_in_label = int(has_labels)
# a=1
# b=c.b+1
a=1
b=2
c,d=1,2
for i in range(2):
    a=1
    if i>1:
        if i>2:
            a=3
        a=2
        break 
if a==2:
    print(1)
print("1")   
def a():
    return 1
for i in range(5):
    a=1
    break
if a:
    print("test")
if __name__ == '__main__':
    a=1
    
'''
    tree = ast.parse(code)
    node_list=[]
    extract_ast_cur_layer_node(tree, node_list)
    for e in node_list:
        print(e)

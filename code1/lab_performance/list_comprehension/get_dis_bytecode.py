# import dis
# def f1():
#     a=[1,2,3,4]
#     l = []
#     for i in a:
#         l.append(i)
# def f2():
#     a = [1, 2, 3, 4]
#     l = [i for i in a]
#
# print(dis.dis(f1) )
# print(dis.dis(f2) )
if __name__ == '__main__':
    a = [1, 2, 3, 4]
    l = []
    for i in a:
        l.append(i)
    a = [1, 2, 3, 4]
    l = [i for i in a]
    code_str='''
a = [1, 2, 3, 4]
l = [i for i in a] 
    '''
    print(globals())
    print(vars())
    code_obj = compile(code_str, '<string>', 'exec')
    print(code_obj)
    # Attributes of code object
    print(dir(code_obj))
    # The filename
    print(code_obj.co_filename)
    # The first chunk of raw bytecode
    print(code_obj.co_code)
    print(code_obj.co_consts)
    # The variable Names
    print(code_obj.co_varnames)

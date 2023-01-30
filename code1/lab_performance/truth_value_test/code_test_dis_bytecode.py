import dis


def func_while():
    a=1
    while a==1:
        break
def func_while_not_equal():
    a=1
    while a!=1:
        break
def func_while_yes():
    a=1
    while a:
        break
def func_while_not():
    a=1
    while not a:
        break
def func_while_pythonic():
    a=1
    while a:
        break
def func_assert():
    a=1
    assert a==1
def func_assert():
    try:
        a=1
        assert a==1
    except:
        a
def func_assert_pythonic():
    a=1
    assert a
def func_0_1():
    a=1
    a==1
def func():
    a=1
    if a:
        pass
def func2():
    a=1
    a
def func_0():
    a=1
    if a==0.0:
        pass
    if not a:
        pass
    if a==range(0):
        pass
    if a==dict():
        pass
if __name__ == '__main__':
    # dis.dis(func_assert)
    dis.dis(func_0)
    # dis.dis(func_assert)
    # dis.dis(func_while)
    # dis.dis(func_while_not)
    # dis.dis(func_while_yes)
    # dis.dis(func_while_not_equal)


    '''
    from fractions import Fraction
    a=Fraction(0, 1)
    print(a)
    for i in range(2):

        a = False
        import time
        start_time_zejun = time.perf_counter()
        if a == False:
            pass
        end_time_zejun = time.perf_counter()
        total_time_zejun = end_time_zejun - start_time_zejun
        print('\n*********zejun test total time************** ', total_time_zejun)
        if a == False:
            pass
    print('code is finished')
    '''
# if __name__ == '__main__':
#     a=()
#     if a==():
#         print("yes")
#     # dis.dis(func_0)
#     # dis.dis(func_0_1)
#     # func_while()
#     # dis.dis(func_while)
#     # dis.dis(func_while_pythonic)
#
#     dis.dis(func_assert)
#     dis.dis(func_assert_pythonic)
#     a = range(0)
#     try:
#         assert a == range(0)
#     except:
#         print("come here")
#
#     print('code is finished')
#
#     # if __name__ == '__main__':
#     for i in range(2):
#
#             a = False
#             import time
#
#             start_time_zejun = time.perf_counter()
#             if not a:
#                 end_time_zejun = time.perf_counter()
#             total_time_zejun = end_time_zejun - start_time_zejun
#             print('\n*********zejun test total time pythonic************** ', total_time_zejun)
#             if a == False:
#                 pass
#
#     print('code is finished')
#
#     # dis.dis(func)
#     # dis.dis(func2)
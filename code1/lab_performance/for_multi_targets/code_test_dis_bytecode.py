import dis
def func_0():
    sales=[1,2,3]
    for item in sales:
        a = item[0], item[1], item[2]
        pass
def func_2_dim():
    for ((e_0_0, e_0_1, *e_0_len), (e_1_0, e_1_1,*e_1_len), *e_len) in sales:
        pass
def func_1():

    sales = [[1,2,3] for i in range(10)]
    for item in sales:
        item[0]
        item[1]
        item[2]
def func_2():

    for item_0,item_1,item_2,*item_len in sales:
        item_0
        item_1
        item_2
    for item_0,item_1,item_2 in sales:
        item_0
        item_1
        item_2


def func_while():
    a=1
    while a==1:
        break
def func_while_pythonic():
    a=1
    while a:
        break
def func_assert():
    a=1
    assert a==1

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
if __name__ == '__main__':
    # pass
    # dis.dis(func_0)
    sales = [[1, 2, 3] for i in range(10)]
    dis.dis(func_1)
    dis.dis(func_2)
    # dis.dis(func_2_dim)
    # sales = [1, 2, 3]
    for item in sales:
        item[0]
        item[1]
        item[2]
    for item_0,item_1,item_2 in sales:
        item_0
        item_2

    # dis.dis(func_while)
    # dis.dis(func_while_pythonic)

    # dis.dis(func_assert)
    # dis.dis(func_assert_pythonic)

    # dis.dis(func)
    # dis.dis(func2)
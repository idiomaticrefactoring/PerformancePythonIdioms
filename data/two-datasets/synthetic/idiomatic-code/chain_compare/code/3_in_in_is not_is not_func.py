def func_a():
    n = 110
    list_0 = [n]
    list_1 = [list_0]
    o = 111
    list_2 = [o]
    list_3 = [list_2]
    p = 112
    list_4 = [p]
    list_5 = [list_4]
    n in list_0 in list_1 is not list_3 is list_5
if __name__ == '__main__':
    func_a()
    print('code is finished')
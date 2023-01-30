def func_a():
    n=110
    o=111
    list_0=[o]
    list_1=[list_0]
    list_2=[list_1]
    p=112
    list_3=[p]
    list_4=[list_3]
    list_5=[list_4]
    n not in list_0 and list_0 not in list_1 and (list_1 in list_2) and (list_2 is not list_5)
if __name__ == '__main__':
    func_a()
    print('code is finished')
def func_a():
    n=110
    o=111
    list_0=[o]
    list_1=[list_0]
    p=112
    list_2=[p]
    list_3=[list_2]
    n < o and o in list_0 and (list_0 in list_1) and (list_1 is list_3)
if __name__ == '__main__':
    func_a()
    print('code is finished')
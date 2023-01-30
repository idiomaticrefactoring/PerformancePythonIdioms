def func_a():
    n=110
    list_0=[n]
    list_1=[list_0]
    o=111
    list_2=[o]
    list_3=[list_2]
    p=112
    list_4=[p]
    list_5=[list_4]
    q=113
    list_6=[q]
    list_7=[list_6]
    n in list_0 and list_0 in list_1 and (list_1 is not list_3) and (list_3 is not list_5) and (list_5 is not list_7)
if __name__ == '__main__':
    func_a()
    print('code is finished')
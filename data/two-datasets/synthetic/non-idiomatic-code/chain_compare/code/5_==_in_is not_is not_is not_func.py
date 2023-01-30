def func_a():
    n=110
    list_0=[n]
    o=111
    list_1=[o]
    p=112
    list_2=[p]
    q=113
    list_3=[q]
    n == n and n in list_0 and (list_0 is not list_1) and (list_1 is not list_2) and (list_2 is not list_3)
if __name__ == '__main__':
    func_a()
    print('code is finished')
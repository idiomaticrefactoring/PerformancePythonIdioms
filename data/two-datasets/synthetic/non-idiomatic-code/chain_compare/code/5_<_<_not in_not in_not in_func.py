def func_a():
    n=110
    o=111
    p=112
    q=113
    list_0=[q]
    list_1=[list_0]
    list_2=[list_1]
    n < o and o < p and (p not in list_0) and (list_0 not in list_1) and (list_1 not in list_2)
if __name__ == '__main__':
    func_a()
    print('code is finished')
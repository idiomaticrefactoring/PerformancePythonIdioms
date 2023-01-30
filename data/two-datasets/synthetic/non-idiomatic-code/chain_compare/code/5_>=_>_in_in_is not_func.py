def func_a():
    n=110
    m=109
    l=108
    list_0=[l]
    list_1=[list_0]
    list_2=[m]
    list_3=[list_2]
    n >= m and m > l and (l in list_0) and (list_0 in list_1) and (list_1 is not list_3)
if __name__ == '__main__':
    func_a()
    print('code is finished')
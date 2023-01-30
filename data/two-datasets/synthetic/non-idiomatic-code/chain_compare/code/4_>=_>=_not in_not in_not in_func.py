def func_a():
    n=110
    m=109
    l=108
    list_0=[m]
    list_1=[list_0]
    list_2=[list_1]
    n >= m and m >= l and (l not in list_0) and (list_0 not in list_1) and (list_1 in list_2)
if __name__ == '__main__':
    func_a()
    print('code is finished')
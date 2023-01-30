def func_a():
    n=110
    o=111
    p=112
    list_0=[p]
    list_1=[list_0]
    n == n and n != o and (o not in list_0) and (list_0 in list_1) and (list_1 is not list_1)
if __name__ == '__main__':
    func_a()
    print('code is finished')
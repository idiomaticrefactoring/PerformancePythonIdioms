def func_a():
    n=110
    list_0=[n]
    list_1=[list_0]
    o=111
    list_2=[o]
    list_3=[list_2]
    n in list_0 and list_0 in list_1 and (list_1 is list_1) and (list_1 is not list_3)
if __name__ == '__main__':
    func_a()
    print('code is finished')
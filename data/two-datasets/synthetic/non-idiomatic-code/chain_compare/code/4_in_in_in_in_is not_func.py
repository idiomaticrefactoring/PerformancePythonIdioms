def func_a():
    n=110
    list_0=[n]
    list_1=[list_0]
    list_2=[list_1]
    list_3=[list_2]
    o=111
    list_4=[o]
    list_5=[list_4]
    list_6=[list_5]
    list_7=[list_6]
    n in list_0 and list_0 in list_1 and (list_1 in list_2) and (list_2 in list_3) and (list_3 is list_7)
if __name__ == '__main__':
    func_a()
    print('code is finished')
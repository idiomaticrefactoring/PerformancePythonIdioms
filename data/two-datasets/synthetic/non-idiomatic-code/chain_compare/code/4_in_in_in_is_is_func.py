def func_a():
    n=110
    list_0=[n]
    list_1=[list_0]
    list_2=[list_1]
    n in list_0 and list_0 in list_1 and (list_1 in list_2) and (list_2 is list_2) and (list_2 is not list_2)
if __name__ == '__main__':
    func_a()
    print('code is finished')
def func_a():
    n = 110
    list_0 = [n]
    list_1 = [list_0]
    list_2 = [list_1]
    list_3 = [list_2]
    n in list_0 in list_1 in list_2 in list_3 is not list_3
if __name__ == '__main__':
    func_a()
    print('code is finished')
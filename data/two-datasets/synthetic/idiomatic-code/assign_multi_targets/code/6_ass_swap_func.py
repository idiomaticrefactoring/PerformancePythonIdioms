def func_a():
    var_1 = 1
    var_2 = 2
    var_3 = 3
    var_4 = 4
    var_5 = 5
    var_6 = 6
    pass
    (var_1, var_2, var_3, var_4, var_5, var_6) = (var_6, var_1, var_2, var_3, var_4, var_5)
if __name__ == '__main__':
    func_a()
    print('code is finished')
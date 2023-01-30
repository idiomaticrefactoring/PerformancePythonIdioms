def func_a():
    var_1 = 1
    var_2 = 2
    var_3 = 3
    var_4 = 4
    pass
    tmp_1 = var_1
    tmp_2 = var_2
    tmp_3 = var_3
    var_1 = var_4
    var_2 = tmp_1
    var_3 = tmp_2
    var_4 = tmp_3
if __name__ == '__main__':
    func_a()
    print('code is finished')
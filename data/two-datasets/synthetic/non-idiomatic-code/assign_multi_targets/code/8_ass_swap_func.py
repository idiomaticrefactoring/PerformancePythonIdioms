def func_a():
    var_1 = 1
    var_2 = 2
    var_3 = 3
    var_4 = 4
    var_5 = 5
    var_6 = 6
    var_7 = 7
    var_8 = 8
    pass
    tmp_1 = var_1
    tmp_2 = var_2
    tmp_3 = var_3
    tmp_4 = var_4
    tmp_5 = var_5
    tmp_6 = var_6
    tmp_7 = var_7
    var_1 = var_8
    var_2 = tmp_1
    var_3 = tmp_2
    var_4 = tmp_3
    var_5 = tmp_4
    var_6 = tmp_5
    var_7 = tmp_6
    var_8 = tmp_7
if __name__ == '__main__':
    func_a()
    print('code is finished')
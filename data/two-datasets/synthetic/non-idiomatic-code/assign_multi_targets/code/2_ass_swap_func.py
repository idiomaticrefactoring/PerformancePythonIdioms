def func_a():
    var_1 = 1
    var_2 = 2
    pass
    tmp_1 = var_1
    var_1 = var_2
    var_2 = tmp_1
if __name__ == '__main__':
    func_a()
    print('code is finished')
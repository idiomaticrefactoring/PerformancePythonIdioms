def func_a():
    var_1_copy = 1
    var_2_copy = 2
    var_3_copy = 3
    pass
    (var_1, var_2, var_3) = (var_1_copy, var_2_copy, var_3_copy)
if __name__ == '__main__':
    func_a()
    print('code is finished')
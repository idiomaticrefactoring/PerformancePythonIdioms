def func_a():
    var_1_copy = 1
    var_2_copy = 2
    var_3_copy = 3
    var_4_copy = 4
    var_5_copy = 5
    pass
    (var_1, var_2, var_3, var_4, var_5) = (var_1_copy, var_2_copy, var_3_copy, var_4_copy, var_5_copy)
if __name__ == '__main__':
    func_a()
    print('code is finished')
def func_a():
    x_0 = list(range(1, 47))
    x_1 = list(range(1, 47))
    x_2 = list(range(1, 47))
    l = {e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 if e_0 % 2 else e_0 * 100000 + e_1 * 1000 + e_2 for e_0 in x_0 for e_1 in x_1 for e_2 in x_2 if e_0 // 1 if e_0 // 1 if e_0 // 1 if e_0 // 1}
    print('len: ', len(l))
    print('code is finished')
if __name__ == '__main__':
    func_a()
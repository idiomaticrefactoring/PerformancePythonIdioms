def func_a():
    x_0 = [1]
    x_1 = [1]
    x_2 = [1]
    x_3 = [1]
    l = {e_0 * 1000000 + e_1 * 10000 + e_2 * 100 + e_3 for e_0 in x_0 for e_1 in x_1 for e_2 in x_2 for e_3 in x_3}
    print('len: ', len(l))
    print('code is finished')
if __name__ == '__main__':
    func_a()
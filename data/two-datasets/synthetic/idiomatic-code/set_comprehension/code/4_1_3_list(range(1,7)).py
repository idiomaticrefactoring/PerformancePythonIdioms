x_0 = list(range(1, 7))
x_1 = list(range(1, 7))
x_2 = list(range(1, 7))
x_3 = list(range(1, 7))
l = {e_0 * 1000000 + e_1 * 10000 + e_2 * 100 + e_3 if e_0 % 2 else e_0 * 1000000 + e_1 * 10000 + e_2 * 100 + e_3 if e_0 % 2 else e_0 * 1000000 + e_1 * 10000 + e_2 * 100 + e_3 if e_0 % 2 else e_0 * 1000000 + e_1 * 10000 + e_2 * 100 + e_3 for e_0 in x_0 for e_1 in x_1 for e_2 in x_2 for e_3 in x_3 if e_0 // 1}
print('len: ', len(l))
print('code is finished')
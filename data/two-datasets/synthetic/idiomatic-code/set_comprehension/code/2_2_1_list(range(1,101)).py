x_0 = list(range(1, 101))
x_1 = list(range(1, 101))
l = {e_0 * 10000 + e_1 if e_0 % 2 else e_0 * 10000 + e_1 for e_0 in x_0 for e_1 in x_1 if e_0 // 1 if e_0 // 1}
print('len: ', len(l))
print('code is finished')
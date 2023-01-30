x_0 = list(range(1, 11))
x_1 = list(range(1, 11))
l = {e_0 * 10000 + e_1: e_0 if e_0 % 2 else e_0 if e_0 % 2 else e_0 for e_0 in x_0 for e_1 in x_1}
print('len: ', len(l))
print('code is finished')
x_0 = list(range(1, 3))
x_1 = list(range(1, 3))
x_2 = list(range(1, 3))
l = {e_0 * 100000 + e_1 * 1000 + e_2 for e_0 in x_0 for e_1 in x_1 for e_2 in x_2}
print('len: ', len(l))
print('code is finished')
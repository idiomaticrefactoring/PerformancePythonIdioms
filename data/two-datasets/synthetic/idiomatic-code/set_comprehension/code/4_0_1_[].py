x_0 = []
x_1 = []
x_2 = []
x_3 = []
l = {e_0 * 1000000 + e_1 * 10000 + e_2 * 100 + e_3 if e_0 % 2 else e_0 * 1000000 + e_1 * 10000 + e_2 * 100 + e_3 for e_0 in x_0 for e_1 in x_1 for e_2 in x_2 for e_3 in x_3}
print('len: ', len(l))
print('code is finished')
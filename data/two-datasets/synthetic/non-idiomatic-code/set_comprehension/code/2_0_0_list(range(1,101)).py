x_0 = list(range(1,101))
x_1 = list(range(1,101))
l = set()
for e_0 in x_0:
    for e_1 in x_1:
        l.add(e_0 * 10000 + e_1)
print('len: ',len(l))
print('code is finished')
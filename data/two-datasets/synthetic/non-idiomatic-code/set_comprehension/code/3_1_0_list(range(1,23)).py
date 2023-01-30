x_0 = list(range(1,23))
x_1 = list(range(1,23))
x_2 = list(range(1,23))
l = set()
for e_0 in x_0:
    for e_1 in x_1:
        for e_2 in x_2:
            if e_0//1:
                l.add(e_0 * 100000 + e_1 * 1000 + e_2)
print('len: ',len(l))
print('code is finished')
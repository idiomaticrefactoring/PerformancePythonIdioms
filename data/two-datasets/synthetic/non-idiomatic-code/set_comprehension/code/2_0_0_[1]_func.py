def func_a():
    x_0 = [1]
    x_1 = [1]
    l = set()
    for e_0 in x_0:
        for e_1 in x_1:
            l.add(e_0 * 10000 + e_1)
    print('len: ',len(l))
    print('code is finished')
if __name__ == '__main__':
    func_a()
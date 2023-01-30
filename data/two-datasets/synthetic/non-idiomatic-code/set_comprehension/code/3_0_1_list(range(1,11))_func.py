def func_a():
    x_0 = list(range(1,11))
    x_1 = list(range(1,11))
    x_2 = list(range(1,11))
    l = set()
    for e_0 in x_0:
        for e_1 in x_1:
            for e_2 in x_2:
                if e_0%2:
                    l.add(e_0 * 100000 + e_1 * 1000 + e_2)
                else:
                    l.add(e_0 * 100000 + e_1 * 1000 + e_2)
    
    print('len: ',len(l))
    print('code is finished')
if __name__ == '__main__':
    func_a()
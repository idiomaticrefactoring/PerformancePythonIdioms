def func_a():
    x_0 = list(range(1,4))
    x_1 = list(range(1,4))
    x_2 = list(range(1,4))
    x_3 = list(range(1,4))
    l = []
    for e_0 in x_0:
        for e_1 in x_1:
            for e_2 in x_2:
                for e_3 in x_3:
                    if e_0//1:
                        if e_0%2:
                            l.append(e_0)
                        else:
                            if e_0%2:
                                l.append(e_0)
                            else:
                                if e_0%2:
                                    l.append(e_0)
                                else:
                                    if e_0%2:
                                        l.append(e_0)
                                    else:
                                        l.append(e_0)
    
    print('len: ',len(l))
    print('code is finished')
if __name__ == '__main__':
    func_a()
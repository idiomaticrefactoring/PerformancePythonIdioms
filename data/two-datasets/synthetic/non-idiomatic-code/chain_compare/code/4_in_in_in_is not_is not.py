
if __name__ == '__main__':
    n=110
    list_0=[n]
    list_1=[list_0]
    list_2=[list_1]
    o=111
    list_3=[o]
    list_4=[list_3]
    list_5=[list_4]
    p=112
    list_6=[p]
    list_7=[list_6]
    list_8=[list_7]
    n in list_0 and list_0 in list_1 and (list_1 in list_2) and (list_2 is not list_5) and (list_5 is list_8)
    print('code is finished')
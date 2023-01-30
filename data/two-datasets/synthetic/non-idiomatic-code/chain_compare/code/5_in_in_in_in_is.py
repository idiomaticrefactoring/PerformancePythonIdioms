
if __name__ == '__main__':
    n=110
    list_0=[n]
    list_1=[list_0]
    list_2=[list_1]
    list_3=[list_2]
    n in list_0 and list_0 in list_1 and (list_1 in list_2) and (list_2 in list_3) and (list_3 is list_3)
    print('code is finished')
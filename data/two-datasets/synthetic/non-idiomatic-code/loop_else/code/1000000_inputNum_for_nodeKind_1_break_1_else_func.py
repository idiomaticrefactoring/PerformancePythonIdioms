def func_a():
    e_list=[i for i in range(1000000)]
    flag=True
    for i in e_list:
        if i==999999:
            flag=False
            break
    if flag==True:
        pass
    else:
        pass

if __name__ == '__main__':
    func_a()
    print('code is finished')
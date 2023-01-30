def func_a():
    e_list=[i for i in range(100000)]
    flag=True
    for i in e_list:
        if i==100000:
            flag=False
            break
    if flag==True:
        pass
    else:
        pass

if __name__ == '__main__':
    func_a()
    print('code is finished')
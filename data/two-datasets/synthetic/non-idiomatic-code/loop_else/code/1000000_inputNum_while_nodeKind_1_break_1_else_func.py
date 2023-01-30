def func_a():
    i=1000000
    flag=True
    while i:
        i-=1
        if i==0:
            flag=False
            break
    if flag==True:
        pass
    else:
        pass

if __name__ == '__main__':
    func_a()
    print('code is finished')
def func_a():
    i=10000
    flag=True
    while i:
        i-=1
        if i==0:
            flag=False
            break
    if flag==True:
        pass

if __name__ == '__main__':
    func_a()
    print('code is finished')
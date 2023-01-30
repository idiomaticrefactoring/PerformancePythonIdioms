def func_a():
    i=1000
    flag=True
    while i:
        i-=1
        if i==-1:
            flag=False
            break
    if flag==True:
        pass

if __name__ == '__main__':
    func_a()
    print('code is finished')
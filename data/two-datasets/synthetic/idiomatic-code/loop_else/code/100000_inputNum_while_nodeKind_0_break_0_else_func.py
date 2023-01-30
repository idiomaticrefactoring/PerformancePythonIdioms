def func_a():
    i = 100000
    while i:
        i -= 1
        if i == -1:
            break
    else:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')
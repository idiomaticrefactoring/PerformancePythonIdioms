def func_a():
    e_list = [i for i in range(10000)]
    for i in e_list:
        if i == 9999:
            break
    else:
        pass
if __name__ == '__main__':
    func_a()
    print('code is finished')
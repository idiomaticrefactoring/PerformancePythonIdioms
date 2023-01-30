def func_arg(*e):
    pass
if __name__ == '__main__':
    e_list = [i for i in range(28)]
    func_arg(
    *e_list[1:3])
    print('code is finished')
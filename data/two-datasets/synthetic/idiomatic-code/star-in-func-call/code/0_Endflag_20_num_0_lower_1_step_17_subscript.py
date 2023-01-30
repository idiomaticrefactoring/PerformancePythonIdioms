def func_arg(*e):
    pass
if __name__ == '__main__':
    e_list = [i for i in range(20)]
    func_arg(
    *e_list[:17])
    print('code is finished')
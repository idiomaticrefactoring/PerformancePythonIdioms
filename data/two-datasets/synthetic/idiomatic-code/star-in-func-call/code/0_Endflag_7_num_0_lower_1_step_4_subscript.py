def func_arg(*e):
    pass
if __name__ == '__main__':
    e_list = [i for i in range(7)]
    func_arg(
    *e_list[:4])
    print('code is finished')
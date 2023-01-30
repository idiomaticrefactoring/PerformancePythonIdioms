def func_arg(*e):
    pass
if __name__ == '__main__':
    e_list = [i for i in range(15)]
    func_arg(
    *e_list)
    print('code is finished')
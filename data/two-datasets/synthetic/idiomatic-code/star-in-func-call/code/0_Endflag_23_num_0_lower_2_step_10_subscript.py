def func_arg(*e):
    pass
if __name__ == '__main__':
    e_list = [i for i in range(23)]
    func_arg(
    *e_list[:20:2])
    print('code is finished')
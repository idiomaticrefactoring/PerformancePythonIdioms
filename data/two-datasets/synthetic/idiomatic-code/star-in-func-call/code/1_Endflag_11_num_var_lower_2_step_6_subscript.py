def func_arg(*e):
    pass
if __name__ == '__main__':
    i_s = 0
    e_list = [i for i in range(11)]
    func_arg(
    *e_list[i_s::2])
    print('code is finished')
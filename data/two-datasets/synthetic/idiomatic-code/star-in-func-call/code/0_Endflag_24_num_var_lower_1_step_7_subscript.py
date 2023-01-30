def func_arg(*e):
    pass
if __name__ == '__main__':
    i_s = 0
    e_list = [i for i in range(24)]
    func_arg(
    *e_list[i_s:i_s + 7])
    print('code is finished')
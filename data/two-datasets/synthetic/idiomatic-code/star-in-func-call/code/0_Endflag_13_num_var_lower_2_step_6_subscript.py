def func_arg(*e):
    pass
if __name__ == '__main__':
    i_s = 0
    e_list = [i for i in range(13)]
    func_arg(
    *e_list[i_s:i_s + 12:2])
    print('code is finished')